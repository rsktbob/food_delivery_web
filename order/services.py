from typing import List
from models import Order
from account.models import BaseUser, CustomerProfile, CourierProfile, VendorProfile

class OrderService:
    def set_order_state(order_id, state):
        pass
    
    def get_order_state(order_id) -> str:
        pass

class CustomerOrderService(OrderService):
    def create_order(user_id,):
        # customer = get_object_or_404(CustomerProfile, user_id=user_id)
        # order = Order.objects.create(
        #     customer=customer,
        #     restaurant=cart.restaurant,
        #     delivery_address=delivery_address,
        #     status='Created',
        #     payment_method=payment_method,
        #     total_price=cart.get_total_price(),
        #     delivery_fee=delivery_fee,
        #     estimated_delivery_time=timezone.now() + timedelta(minutes=45)
        # )
        pass

class VendorOrderService(OrderService):
    def get_restaurant_orders(restaurant_id) -> List[Order]:
        pass
    
    def accept_restaurant_order(order_id) -> bool:
        pass

    def finish_restaurant_order(order_id) -> bool:
        pass

class CourierOrderService(OrderService):
    def search_nearby_order() -> List[Order]: #導航先不寫
        pass

    def accept_for_delivery():
        pass

    def nevigation(position):
        pass