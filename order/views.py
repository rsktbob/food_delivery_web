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
from services import CustomerOrderService, VendorOrderService, CourierOrderService

class OrderManageHandler:
    customerOrderService = CustomerOrderService()
    VendorOrderService = VendorOrderService()
    CourierOrderService = CourierOrderService()

    @classmethod
    def createOrder(cls, request):
        request
        cls.customerOrderService.create_order(request)
    
    @classmethod
    def setOrderState(cls, request):
        cls.customerOrderService.set_order_state(request)
    
    @classmethod
    def getOrderState(cls, request):
        cls.customerOrderService.get_order_state(request)  
      
    @classmethod
    def checkCourierOrder(cls, request):
        cls.CourierOrderService.search_nearby_order(request)

    @classmethod
    def checkVendorOrder(cls, request):
        cls.VendorOrderService.get_restaurant_orders(request)

    @classmethod
    def acceptVendorOrder(cls, request):
        cls.VendorOrderService.accept_restaurant_order(request)
        
    @classmethod
    def finishOrder(cls, request):
        cls.VendorOrderService.finish_restaurant_order(request)
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

def get_order_state(request, order_id):
    """Get the current state of an order"""
    try:
        # Check if the user is the customer, courier, or restaurant owner
        if request.user.is_authenticated:
            order = Order.objects.get(id=order_id)
            
            # Verify permission to view this order
            if (order.customer == request.user or 
                (order.courier and order.courier.user == request.user) or
                order.restaurant.owner == request.user):
                
                response_data = {
                    'id': order.id,
                    'status': order.status,
                    'restaurant': {
                        'id': order.restaurant.id,
                        'name': order.restaurant.name,
                        'address': order.restaurant.address,
                        'latitude': order.restaurant.latitude,
                        'longitude': order.restaurant.longitude
                    },
                    'delivery_address': {
                        'address': order.delivery_address.address_line1,
                        'city': order.delivery_address.city,
                        'latitude': order.delivery_address.latitude,
                        'longitude': order.delivery_address.longitude
                    },
                    'courier': None,
                    'total': float(order.grand_total),
                    'created_at': order.created_at.isoformat(),
                    'estimated_delivery_time': order.estimated_delivery_time.isoformat() if order.estimated_delivery_time else None
                }
                
                if order.courier:
                    response_data['courier'] = {
                        'name': order.courier.user.get_full_name() or order.courier.user.username,
                        'latitude': order.courier.current_latitude,
                        'longitude': order.courier.current_longitude,
                        'phone': order.courier.user.phone_number
                    }
                
                return JsonResponse(response_data)
            
        return JsonResponse({'error': 'Not authorized to view this order'}, status=403)
    
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def set_order_state(request, order_id):
    """Update order status"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if not new_status:
            return JsonResponse({'error': 'Status is required'}, status=400)
        
        order = get_object_or_404(Order, id=order_id)
        
        # Check permissions based on status
        user = request.user
        current_status = order.status
        
        # Restaurant owner permissions
        if order.restaurant.owner == user:
            if new_status in ['confirmed', 'preparing', 'ready_for_pickup']:
                order.status = new_status
                if new_status == 'confirmed':
                    # Estimate delivery time, e.g., 45 minutes from now
                    order.estimated_delivery_time = timezone.now() + timezone.timedelta(minutes=45)
                order.save()
                return JsonResponse({'success': True, 'status': new_status})
            else:
                return JsonResponse({'error': 'Invalid status for restaurant owner'}, status=403)
                
        # Courier permissions
        elif hasattr(user, 'courier_profile') and order.courier and order.courier.user == user:
            if new_status in ['picked_up', 'on_delivery', 'delivered']:
                order.status = new_status
                order.save()
                return JsonResponse({'success': True, 'status': new_status})
            else:
                return JsonResponse({'error': 'Invalid status for courier'}, status=403)
        
        # Customer permissions
        elif order.customer == user:
            if new_status == 'cancelled' and current_status in ['pending', 'confirmed']:
                order.status = new_status
                order.save()
                return JsonResponse({'success': True, 'status': new_status})
            else:
                return JsonResponse({'error': 'Invalid status for customer'}, status=403)
        
        else:
            return JsonResponse({'error': 'Not authorized to update this order'}, status=403)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def check_courier_order(order):
    """Find and assign a courier to the order"""
    # Find available couriers near the restaurant
    restaurant = order.restaurant
    available_couriers = CourierProfile.objects.filter(
        is_available=True
    ).exclude(
        current_latitude__isnull=True
    ).exclude(
        current_longitude__isnull=True
    )
    
    if not available_couriers:
        return False
    
    # Find the closest courier
    closest_courier = None
    min_distance = float('inf')
    
    for courier in available_couriers:
        distance = calculate_distance(
            restaurant.latitude, 
            restaurant.longitude,
            courier.current_latitude,
            courier.current_longitude
        )
        
        if distance < min_distance:
            min_distance = distance
            closest_courier = courier
    
    # Assign courier if found and within reasonable distance (e.g., 10km)
    if closest_courier and min_distance < 10:
        order.courier = closest_courier
        order.save()
        return True
    
    return False

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Radius of earth in km
    
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    
    a = sin(dLat/2) * sin(dLat/2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon/2) * sin(dLon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    distance = R * c
    return distance

@login_required
def check_vendor_order(request):
    """Get list of orders for a restaurant owner"""
    if not request.user.is_vendor():
        return JsonResponse({'error': 'Not authorized'}, status=403)
    
    try:
        restaurants = Restaurant.objects.filter(owner=request.user)
        if not restaurants.exists():
            return JsonResponse({'orders': []})
        
        restaurant_ids = [r.id for r in restaurants]
        orders = Order.objects.filter(
            restaurant_id__in=restaurant_ids
        ).exclude(
            status__in=['delivered', 'cancelled']
        ).order_by('-created_at')
        
        orders_data = []
        for order in orders:
            items = []
            for item in order.items.all():
                items.append({
                    'name': item.menu_item.name,
                    'quantity': item.quantity,
                    'special_instructions': item.special_instructions,
                    'customizations': [
                        f"{c.option_name}: {c.choice_name}" 
                        for c in item.customizations.all()
                    ]
                })
            
            orders_data.append({
                'id': order.id,
                'status': order.status,
                'customer_name': order.customer.get_full_name() or order.customer.username,
                'created_at': order.created_at.isoformat(),
                'items': items,
                'total': float(order.grand_total)
            })
        
        return JsonResponse({'orders': orders_data})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def accept_vendor_order(request, order_id):
    """Restaurant accepts an order"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if not request.user.is_vendor():
        return JsonResponse({'error': 'Not authorized'}, status=403)
    
    try:
        order = get_object_or_404(Order, id=order_id)
        
        # Verify the user owns this restaurant
        if order.restaurant.owner != request.user:
            return JsonResponse({'error': 'Not authorized to accept this order'}, status=403)
        
        if order.status != 'pending':
            return JsonResponse({'error': f'Order is already {order.status}'}, status=400)
        
        order.status = 'confirmed'
        # Set estimated delivery time
        order.estimated_delivery_time = timezone.now() + timezone.timedelta(minutes=45)
        order.save()
        
        return JsonResponse({'success': True, 'status': 'confirmed'})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def finish_order(request, order_id):
    """Restaurant marks order as ready for pickup"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if not request.user.is_vendor():
        return JsonResponse({'error': 'Not authorized'}, status=403)
    
    try:
        order = get_object_or_404(Order, id=order_id)
        
        # Verify the user owns this restaurant
        if order.restaurant.owner != request.user:
            return JsonResponse({'error': 'Not authorized to update this order'}, status=403)
        
        if order.status not in ['confirmed', 'preparing']:
            return JsonResponse({'error': f'Cannot mark as ready: order is {order.status}'}, status=400)
        
        order.status = 'ready_for_pickup'
        order.save()
        
        return JsonResponse({'success': True, 'status': 'ready_for_pickup'})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def navigation(request):
    """Return navigation data for a courier's current delivery"""
    if not request.user.is_courier():
        return JsonResponse({'error': 'Not authorized'}, status=403)
    
    try:
        courier_profile = request.user.courier_profile
        
        # Update courier location
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        
        if lat and lon:
            courier_profile.current_latitude = float(lat)
            courier_profile.current_longitude = float(lon)
            courier_profile.save()
        
        # Get the courier's active delivery
        active_order = Order.objects.filter(
            courier=courier_profile,
            status__in=['confirmed', 'preparing', 'ready_for_pickup', 'picked_up', 'on_delivery']
        ).first()
        
        if not active_order:
            return JsonResponse({'has_active_order': False})
        
        # Determine destination based on order status
        if active_order.status in ['confirmed', 'preparing', 'ready_for_pickup']:
            # Navigate to restaurant
            destination = {
                'name': active_order.restaurant.name,
                'address': active_order.restaurant.address,
                'latitude': active_order.restaurant.latitude,
                'longitude': active_order.restaurant.longitude,
            }
            instruction = "Pick up order from restaurant"
        else:
            # Navigate to customer
            destination = {
                'address': active_order.delivery_address.address_line1,
                'city': active_order.delivery_address.city,
                'latitude': active_order.delivery_address.latitude,
                'longitude': active_order.delivery_address.longitude,
            }
            instruction = "Deliver order to customer"
        
        return JsonResponse({
            'has_active_order': True,
            'order_id': active_order.id,
            'status': active_order.status,
            'destination': destination,
            'instruction': instruction
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
