from typing import List
from models import Order

class OrderService:
    def set_order_state(order_id, state):
        pass
    
    def get_order_state(order_id) -> str:
        pass

class CustomerOrderService(OrderService):
    def create_order(user_id):
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