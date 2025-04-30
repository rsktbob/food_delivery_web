from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import Cart, CartItem, CartItemCustomization, Order, OrderItem, OrderItemCustomization
from Restaurant.models import Restaurant, MenuItem, CustomizationChoice
from account.models import Address, CourierProfile, BaseUser
from django.utils import timezone
import json
from services import *

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
    # vendor finish order
    def finishOrder(cls, request):
        success = cls.VendorOrderService.finish_restaurant_order(request)
        if success:
            return JsonResponse({'status': 'success', 'message': 'Order finished successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to finish the order.'})

# @login_required
# def add_to_shopping_cart(request):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
    
#     try:
#         data = json.loads(request.POST.get()
#         menu_item_id = data.get('menu_item_id')
#         quantity = data.get('quantity', 1)
#         customizations = data.get('customizations', [])
#         special_instructions = data.get('special_instructions', '')
        
#         menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        
#         # Get or create user's cart
#         cart, created = Cart.objects.get_or_create(customer=request.user)
        
#         # Check if adding from a different restaurant
#         if cart.restaurant and cart.restaurant != menu_item.restaurant:
#             return JsonResponse({
#                 'error': 'You already have items from a different restaurant in your cart',
#                 'current_restaurant': cart.restaurant.name
#             }, status=400)
        
#         # Set the restaurant if cart is empty
#         if not cart.restaurant:
#             cart.restaurant = menu_item.restaurant
#             cart.save()
        
#         # Create cart item
#         cart_item = CartItem.objects.create(
#             cart=cart,
#             menu_item=menu_item,
#             quantity=quantity,
#             special_instructions=special_instructions
#         )
        
#         # Add customizations
#         for custom in customizations:
#             choice_id = custom.get('choice_id')
#             if choice_id:
#                 choice = get_object_or_404(CustomizationChoice, id=choice_id)
#                 CartItemCustomization.objects.create(
#                     cart_item=cart_item,
#                     choice=choice
#                 )
        
#         return JsonResponse({
#             'success': True,
#             'cart_item_id': cart_item.id,
#             'cart_total': cart.get_total_price()
#         })
        
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)

# @login_required
# def get_cart(request):
#     try:
#         cart = Cart.objects.get(customer=request.user)
#         items = []
        
#         for item in cart.cartitem_set.all():
#             customizations = []
#             for custom in item.cartitemcustomization_set.all():
#                 customizations.append({
#                     'option_name': custom.choice.option.name,
#                     'choice_name': custom.choice.name,
#                     'additional_price': float(custom.choice.additional_price)
#                 })
            
#             items.append({
#                 'id': item.id,
#                 'menu_item_id': item.menu_item.id,
#                 'name': item.menu_item.name,
#                 'quantity': item.quantity,
#                 'unit_price': float(item.menu_item.price),
#                 'total_price': float(item.get_total_price()),
#                 'special_instructions': item.special_instructions,
#                 'customizations': customizations
#             })
        
#         return JsonResponse({
#             'success': True,
#             'restaurant': {
#                 'id': cart.restaurant.id,
#                 'name': cart.restaurant.name
#             } if cart.restaurant else None,
#             'items': items,
#             'total': float(cart.get_total_price())
#         })
        
#     except Cart.DoesNotExist:
#         return JsonResponse({
#             'success': True,
#             'restaurant': None,
#             'items': [],
#             'total': 0
#         })

# @login_required
# @require_POST
# def create_order(request):
#     try:
#         data = json.loads(request.body)
#         address_id = data.get('address_id')
#         payment_method = data.get('payment_method')
        
#         # Get user's cart
#         cart = get_object_or_404(Cart, customer=request.user)
        
#         if not cart.cartitem_set.exists():
#             return JsonResponse({'error': 'Your cart is empty'}, status=400)
        
#         # Get delivery address
#         address = get_object_or_404(Address, id=address_id, user=request.user)
        
#         with transaction.atomic():
#             # Create order
#             order = Order.objects.create(
#                 customer=request.user,
#                 restaurant=cart.restaurant,
#                 delivery_address=address,
#                 payment_method=payment_method,
#                 total_price=0,  # Will be calculated later
#                 delivery_fee=5.00,  # Example fixed fee
#                 tax=0,  # Will be calculated later
#                 grand_total=0  # Will be calculated later
#             )
            
#             # Create order items from cart items
#             for cart_item in cart.cartitem_set.all():
#                 order_item = OrderItem.objects.create(
#                     order=order,
#                     menu_item=cart_item.menu_item,
#                     quantity=cart_item.quantity,
#                     unit_price=cart_item.menu_item.price,
#                     special_instructions=cart_item.special_instructions
#                 )
                
#                 # Add customizations
#                 for cart_customization in cart_item.cartitemcustomization_set.all():
#                     OrderItemCustomization.objects.create(
#                         order_item=order_item,
#                         option_name=cart_customization.choice.option.name,
#                         choice_name=cart_customization.choice.name,
#                         additional_price=cart_customization.choice.additional_price
#                     )
            
#             # Calculate totals
#             order.calculate_totals()
            
#             # Clear the cart
#             cart.clear()
            
#             # Check for available couriers
#             check_courier_order(order)
            
#             return JsonResponse({
#                 'success': True,
#                 'order_id': order.id,
#                 'status': order.status
#             })
            
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)

