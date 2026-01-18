"""Remove from cart use case"""
from interfaces.repositories.cart_repository import CartRepository


class RemoveFromCartUseCase:
    """Use case for removing item from cart"""
    
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository
    
    def execute(self, item_id: int) -> str:
        """
        Remove item from cart
        Returns: error_message (None if success)
        """
        try:
            self.cart_repository.remove_item(item_id)
            return None
        except Exception as e:
            return str(e)
