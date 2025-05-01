from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem
from Restaurant.models import Restaurant, MenuItem
from account.models import CourierProfile, BaseUser
from django.utils import timezone
import json
from .services import *

class OrderManageHandler:
    CustomerOrderService = CustomerOrderService()
    VendorOrderService = VendorOrderService()
    CourierOrderService = CourierOrderService()

    @classmethod
    def createOrder(cls, request):
        user = request.user
        user_id = user.id

        # 從前端取得資料
        restaurant_id = request.POST.get('restaurant_id')
        delivery_address = request.POST.get('delivery_address')
        total_price = float(request.POST.get('total_price', 0))  # 默認為 0
        payment_method = request.POST.get('payment_method')
        delivery_fee = float(request.POST.get('delivery_fee', 0))  # 默認為 0

        # 根據 restaurant_id 取得對應的餐廳實例
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        # 創建訂單信息字典
        order_info = {
            'user_id': user_id,
            'restaurant_id': restaurant,
            'delivery_address': delivery_address,
            'total_price': total_price,
            'payment_method': payment_method,
            'delivery_fee': delivery_fee
        }

        # 呼叫服務層創建訂單
        success = cls.CustomerOrderService.create_order(order_info)

        # 返回相應的 JsonResponse
        if success:
            return JsonResponse({'status': 'success', 'message': 'Order created successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to create order.'}, status=400)
  
    @classmethod
    def setOrderState(cls, request):
        order_id = request.POST.get('order_id')  # 假設訂單 ID 傳遞過來
        state = request.POST.get('state')  # 新的訂單狀態
        
        success = cls.CustomerOrderService.set_order_state(order_id, state)
        if success:
            return JsonResponse({'status': 'success', 'message': 'Order state updated successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to update order state.'}, status=400)
        
    
    @classmethod
    def getOrderState(cls, request):
        # 從 POST 請求中獲取訂單 ID
        order_id = request.POST.get('order_id')
        
        order_state = cls.CustomerOrderService.get_order_state(order_id)
        if order_state is not None:
            return JsonResponse({'status': 'success', 'order_state': order_state})
        else:
            return JsonResponse({'status': 'error', 'message': 'Order not found.'}, status=404)
        
    @classmethod
    def checkCourierOrder(cls, request):
        nearby_orders = cls.CourierOrderService.search_nearby_order()
        if nearby_orders:
            return JsonResponse({'status': 'success', 'nearby_orders': nearby_orders})
        else:
            return JsonResponse({'status': 'info', 'message': 'No nearby orders found.'})

    @classmethod
    def checkVendorOrder(cls, request):
        restaurant_id = request.POST.get('restaurant_id')
        
        orders = cls.VendorOrderService.get_restaurant_orders(restaurant_id)
        if orders:
            return JsonResponse({'status': 'success', 'orders': orders})
        else:
            return JsonResponse({'status': 'info', 'message': 'No orders found for this restaurant.'})

    @classmethod
    def acceptVendorOrder(cls, request):
        order_id = request.POST.get('order_id')
        success = cls.VendorOrderService.accept_restaurant_order(order_id)
        if success:
            return JsonResponse({'status': 'success', 'message': 'Order accepted successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to accept the order.'})
        
    @classmethod
    def finishOrder(cls, request):
        order_id = request.POST.get('order_id')
        success = cls.CourierOrderService.finish_restaurant_order(order_id)
        if success:
            return JsonResponse({'status': 'success', 'message': 'Order finished successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to finish the order.'})

