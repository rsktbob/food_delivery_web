from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from unittest.mock import patch, MagicMock

from order.models import Order, OrderItem
from account.models import CustomerProfile, CourierProfile, VendorProfile
from Restaurant.models import Restaurant, MenuItem
from order.services import CustomerOrderService, VendorOrderService, CourierOrderService
from order.views import OrderManageHandler

User = get_user_model()

class OrderManageHandlerTestCase(TestCase):
    """Test the OrderManageHandler methods directly"""
    
    def setUp(self):
        """Set up test data - more compact setup with essential objects only"""
        # Create users
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
        
        # Create profiles
        self.customer = CustomerProfile.objects.create(
            user=self.customer_user, save_address='123 Test St'
        )
        self.vendor = VendorProfile.objects.create(
            user=self.vendor_user, restaurant_name='Test Restaurant'
        )
        self.courier = CourierProfile.objects.create(
            user=self.courier_user, vehicle_type='Scooter'
        )
        
        # Create restaurant and menu items
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant', address='456 Test Ave', owner=self.vendor
        )
        self.menu_item1 = MenuItem.objects.create(
            restaurant=self.restaurant, name='Test Burger', price=Decimal('10.99')
        )
        self.menu_item2 = MenuItem.objects.create(
            restaurant=self.restaurant, name='Test Fries', price=Decimal('4.99')
        )
        
        # Create order and order items
        self.order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address='123 Test St',
            status='Created',
            payment_method='Credit Card',
            total_price=Decimal('15.98'),
            delivery_fee=Decimal('3.00')
        )
        OrderItem.objects.create(
            order=self.order, menu_item=self.menu_item1, 
            quantity=1, unit_price=self.menu_item1.price
        )
        OrderItem.objects.create(
            order=self.order, menu_item=self.menu_item2,
            quantity=1, unit_price=self.menu_item2.price
        )
        
        # Create a mock request
        self.request = MagicMock()
        self.request.user = self.customer_user
        self.request.POST = {}
    
    def _set_request_post_data(self, data):
        """Helper method to set request POST data"""
        self.request.POST = data
        
    def _assert_success_response(self, response, message=None):
        """Helper method to check success response"""
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('"status": "success"', content)
        if message:
            self.assertIn(f'"message": "{message}"', content)
    
    def _assert_error_response(self, response, status_code, message=None):
        """Helper method to check error response"""
        self.assertEqual(response.status_code, status_code)
        content = response.content.decode()
        self.assertIn('"status": "error"', content)
        if message:
            self.assertIn(f'"message": "{message}"', content)
    
    @patch.object(CustomerOrderService, 'create_order')
    def test_create_order(self, mock_create_order):
        """Test createOrder method with both success and failure cases"""
        test_data = {
            'restaurant_id': str(self.restaurant.id),
            'delivery_address': '789 New Address',
            'total_price': '25.98',
            'payment_method': 'Cash',
            'delivery_fee': '4.00'
        }
        
        # Test success case
        mock_create_order.return_value = True
        self._set_request_post_data(test_data)
        response = OrderManageHandler.createOrder(self.request)
        self._assert_success_response(response, "Order created successfully!")
        mock_create_order.assert_called_once()
        
        # Test failure case
        mock_create_order.reset_mock()
        mock_create_order.return_value = False
        response = OrderManageHandler.createOrder(self.request)
        self._assert_error_response(response, 400, "Failed to create order.")
    
    @patch.object(CustomerOrderService, 'set_order_state')
    def test_set_order_state(self, mock_set_order_state):
        """Test setOrderState method with both success and failure cases"""
        test_data = {
            'order_id': str(self.order.id),
            'state': 'Accepted'
        }
        
        # Test success case
        mock_set_order_state.return_value = True
        self._set_request_post_data(test_data)
        response = OrderManageHandler.setOrderState(self.request)
        self._assert_success_response(response, "Order state updated successfully!")
        mock_set_order_state.assert_called_once_with(str(self.order.id), 'Accepted')
        
        # Test failure case
        mock_set_order_state.reset_mock()
        mock_set_order_state.return_value = False
        response = OrderManageHandler.setOrderState(self.request)
        self._assert_error_response(response, 400, "Failed to update order state.")
    
    @patch.object(CustomerOrderService, 'get_order_state')
    def test_get_order_state(self, mock_get_order_state):
        """Test getOrderState method for both found and not found cases"""
        self._set_request_post_data({'order_id': str(self.order.id)})
        
        # Test order found case
        mock_get_order_state.return_value = 'Accepted'
        response = OrderManageHandler.getOrderState(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('"order_state": "Accepted"', response.content.decode())
        mock_get_order_state.assert_called_once_with(str(self.order.id))
        
        # Test order not found case
        mock_get_order_state.reset_mock()
        mock_get_order_state.return_value = None
        response = OrderManageHandler.getOrderState(self.request)
        self._assert_error_response(response, 404, "Order not found.")
    
    @patch.object(CourierOrderService, 'search_nearby_order')
    def test_check_courier_order(self, mock_search_nearby_order):
        """Test checkCourierOrder method for both with and without orders cases"""
        # Set courier user
        self.request.user = self.courier_user
        
        # Test orders found case
        mock_order_data = [{'id': self.order.id, 'status': 'Accepted'}]
        mock_search_nearby_order.return_value = mock_order_data
        response = OrderManageHandler.checkCourierOrder(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('"nearby_orders":', response.content.decode())
        
        # Test no orders found case
        mock_search_nearby_order.return_value = []
        response = OrderManageHandler.checkCourierOrder(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('"message": "No nearby orders found."', response.content.decode())
    
    @patch.object(VendorOrderService, 'get_restaurant_orders')
    def test_check_vendor_order(self, mock_get_restaurant_orders):
        """Test checkVendorOrder method for both with and without orders cases"""
        # Set vendor user and request data
        self.request.user = self.vendor_user
        self._set_request_post_data({'restaurant_id': str(self.restaurant.id)})
        
        # Test orders found case
        mock_order_data = [{'id': self.order.id, 'status': 'Created'}]
        mock_get_restaurant_orders.return_value = mock_order_data
        response = OrderManageHandler.checkVendorOrder(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('"orders":', response.content.decode())
        
        # Test no orders found case
        mock_get_restaurant_orders.return_value = []
        response = OrderManageHandler.checkVendorOrder(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('"message": "No orders found for this restaurant."', response.content.decode())
    
    @patch.object(VendorOrderService, 'accept_restaurant_order')
    def test_accept_vendor_order(self, mock_accept_restaurant_order):
        """Test acceptVendorOrder method with both success and failure cases"""
        # Set vendor user and request data
        self.request.user = self.vendor_user
        self._set_request_post_data({'order_id': str(self.order.id)})
        
        # Test success case
        mock_accept_restaurant_order.return_value = True
        response = OrderManageHandler.acceptVendorOrder(self.request)
        self._assert_success_response(response, "Order accepted successfully.")
        
        # Test failure case
        mock_accept_restaurant_order.return_value = False
        response = OrderManageHandler.acceptVendorOrder(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('"message": "Failed to accept the order."', response.content.decode())
    
    @patch.object(CourierOrderService, 'finish_restaurant_order')
    def test_finish_order(self, mock_finish_restaurant_order):
        """Test finishOrder method with both success and failure cases"""
        # Set courier user and request data
        self.request.user = self.courier_user
        self._set_request_post_data({'order_id': str(self.order.id)})
        
        # Test success case
        mock_finish_restaurant_order.return_value = True
        response = OrderManageHandler.finishOrder(self.request)
        self._assert_success_response(response, "Order finished successfully.")
        
        # Test failure case
        mock_finish_restaurant_order.return_value = False
        response = OrderManageHandler.finishOrder(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('"message": "Failed to finish the order."', response.content.decode())