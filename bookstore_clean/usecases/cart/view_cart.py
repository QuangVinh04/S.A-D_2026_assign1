"""View cart use case"""
from domain.entities.cart import Cart
from interfaces.repositories.cart_repository import CartRepository


class ViewCartUseCase:
    """Use case for viewing cart"""
    
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository
    
    def execute(self, customer_id: int) -> Cart:
        """Get cart for customer"""
        return self.cart_repository.get_or_create_cart(customer_id)
