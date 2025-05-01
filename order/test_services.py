from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from unittest.mock import patch

from order.models import Order, OrderItem, Cart, CartItem
from account.models import CustomerProfile, CourierProfile, VendorProfile
from Restaurant.models import Restaurant, MenuItem
from order.services import OrderService, CustomerOrderService, VendorOrderService, CourierOrderService

User = get_user_model()

class OrderServiceTestCase(TestCase):
    def setUp(self):
        # 创建基础用户
        self.customer_user = User.objects.create_user(
            username='testcustomer', email='customer@test.com',
            password='password123', user_type='customer'
        )
        self.vendor_user = User.objects.create_user(
            username='testvendor', email='vendor@test.com',
            password='password123', user_type='vendor'
        )
        self.courier_user = User.objects.create_user(
            username='testcourier', email='courier@test.com',
            password='password123', user_type='courier'
        )
        
        # 创建用户档案
        self.customer = CustomerProfile.objects.create(
            user=self.customer_user, save_address='123 Test St'
        )
        self.vendor = VendorProfile.objects.create(
            user=self.vendor_user, restaurant_name='Test Restaurant'
        )
        self.courier = CourierProfile.objects.create(
            user=self.courier_user, vehicle_type='Scooter'
        )
        
        # 创建餐厅
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant', address='456 Test Ave', owner=self.vendor
        )
        
        # 创建菜单项
        self.menu_item1 = MenuItem.objects.create(
            restaurant=self.restaurant, name='Test Burger', price=Decimal('10.99')
        )
        self.menu_item2 = MenuItem.objects.create(
            restaurant=self.restaurant, name='Test Fries', price=Decimal('4.99')
        )
        
        # 创建订单
        self.order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address='123 Test St',
            status='Created',
            payment_method='Credit Card',
            total_price=Decimal('15.98'),
            delivery_fee=Decimal('3.00')
        )
        
        # 创建订单项
        self.order_item1 = OrderItem.objects.create(
            order=self.order, menu_item=self.menu_item1, 
            quantity=1, unit_price=self.menu_item1.price
        )
        self.order_item2 = OrderItem.objects.create(
            order=self.order, menu_item=self.menu_item2,
            quantity=1, unit_price=self.menu_item2.price
        )
        
        # 创建购物车
        self.cart = Cart.objects.create(
            customer=self.customer, restaurant=self.restaurant
        )
        self.cart_item1 = CartItem.objects.create(
            cart=self.cart, menu_item=self.menu_item1, quantity=1
        )
        self.cart_item2 = CartItem.objects.create(
            cart=self.cart, menu_item=self.menu_item2, quantity=1
        )
        
        # 初始化服务
        self.order_service = OrderService()
        self.customer_order_service = CustomerOrderService()
        self.vendor_order_service = VendorOrderService()
        self.courier_order_service = CourierOrderService()
        
        # 测试用订单信息
        self.order_info = {
            'user_id': self.customer_user.id,
            'restaurant_id': self.restaurant.id,
            'delivery_address': '789 New Address',
            'payment_method': 'Cash',
            'total_price': Decimal('25.98'),
            'delivery_fee': Decimal('4.00'),
        }

    def test_base_order_service(self):
        result = self.order_service.set_order_state(self.order.id, 'Accepted')
        self.assertTrue(result)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Accepted')
        
        status = self.order_service.get_order_state(self.order.id)
        self.assertEqual(status, 'Accepted')
        
        self.assertFalse(self.order_service.set_order_state(999, 'Accepted'))
        self.assertIsNone(self.order_service.get_order_state(999))
        
        with patch('order.models.Order.objects.get', side_effect=Exception('Random error')):
            self.assertFalse(self.order_service.set_order_state(self.order.id, 'Created'))
            self.assertIsNone(self.order_service.get_order_state(self.order.id))

    def test_customer_order_service(self):
        result = self.customer_order_service.create_order(self.order_info)
        self.assertTrue(result)
        
        order = Order.objects.filter(
            customer=self.customer,
            delivery_address='789 New Address'
        ).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.status, 'Created')
        
        invalid_info = self.order_info.copy()
        invalid_info['user_id'] = 999
        self.assertFalse(self.customer_order_service.create_order(invalid_info))
        
        invalid_info = self.order_info.copy()
        invalid_info['restaurant_id'] = 999
        self.assertFalse(self.customer_order_service.create_order(invalid_info))
        
        incomplete_info = {'user_id': self.customer_user.id}
        self.assertFalse(self.customer_order_service.create_order(incomplete_info))
        
        with patch('account.models.CustomerProfile.objects.get', side_effect=Exception('Random error')):
            self.assertFalse(self.customer_order_service.create_order(self.order_info))

    def test_vendor_order_service(self):
        """测试商家订单服务"""
        # 测试获取餐厅订单
        orders = self.vendor_order_service.get_restaurant_orders(self.restaurant.id)
        self.assertEqual(orders.count(), 1)
        self.assertEqual(orders.first(), self.order)
        
        # 测试接受订单
        result = self.vendor_order_service.accept_restaurant_order(self.order.id)
        self.assertTrue(result)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Accepted')
        
        # 测试无效餐厅ID和订单ID
        self.assertEqual(self.vendor_order_service.get_restaurant_orders(999).count(), 0)
        self.assertFalse(self.vendor_order_service.accept_restaurant_order(999))
        
        # 测试异常情况
        with patch.object(VendorOrderService, 'set_order_state', return_value=False):
            self.assertFalse(self.vendor_order_service.accept_restaurant_order(self.order.id))

    def test_courier_order_service(self):
        """测试快递员订单服务"""
        # 设置订单状态为已接受
        self.order.status = 'Accepted'
        self.order.save()
        
        # 测试查找附近订单
        orders = self.courier_order_service.search_nearby_order()
        self.assertEqual(orders.count(), 1)
        self.assertEqual(orders.first(), self.order)
        
        # 测试接受配送
        result = self.courier_order_service.accept_for_delivery(self.order.id)
        self.assertTrue(result)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Assigned')
        
        # 测试取餐
        result = self.courier_order_service.pick_up_meal(self.order.id)
        self.assertTrue(result)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Picked_Up')
        
        # 测试完成订单
        result = self.courier_order_service.finish_restaurant_order(self.order.id)
        self.assertTrue(result)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'Finish')
        
        # 测试无效状态
        self.order.status = 'Created'
        self.order.save()
        self.assertFalse(self.courier_order_service.accept_for_delivery(self.order.id))
        self.assertFalse(self.courier_order_service.pick_up_meal(self.order.id))
        self.assertFalse(self.courier_order_service.finish_restaurant_order(self.order.id))
        
        # 测试导航方法
        self.assertIsNone(self.courier_order_service.nevigation("Test Location"))
        self.assertIsNone(self.courier_order_service.nevigation({"lat": 25.0, "lng": 121.5}))

    def test_model_methods(self):
        """测试模型方法"""
        # 测试购物车总价
        total_price = self.cart.get_total_price()
        expected_total = self.menu_item1.price + self.menu_item2.price
        self.assertEqual(total_price, expected_total)
        
        # 测试购物车清空
        self.cart.clear()
        self.assertEqual(self.cart.cartitem_set.count(), 0)
        self.assertIsNone(self.cart.restaurant)
        
        # 测试购物车项目总价
        self.cart_item1 = CartItem.objects.create(
            cart=self.cart, menu_item=self.menu_item1, quantity=3
        )
        self.assertEqual(self.cart_item1.get_total_price(), self.menu_item1.price * 3)
        
        # 测试订单项目总价
        self.order_item1.quantity = 2
        self.order_item1.save()
        self.assertEqual(self.order_item1.get_total_price(), self.menu_item1.price * 2)
        
        # 测试订单计算总额
        if hasattr(self.order, 'calculate_totals'):
            self.order.total_price = Decimal('0.00')
            self.order.save()
            self.order.calculate_totals()
            expected_price = self.order_item1.get_total_price() + self.order_item2.get_total_price()
            self.assertEqual(self.order.total_price, expected_price)
            if hasattr(self.order, 'grand_total'):
                self.assertEqual(self.order.grand_total, expected_price + self.order.delivery_fee)