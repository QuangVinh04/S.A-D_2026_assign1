"""Cart repository interface"""
from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.cart import Cart, CartItem


class CartRepository(ABC):
    """Interface for cart repository"""
    
    @abstractmethod
    def get_or_create_cart(self, customer_id: int) -> Cart:
        """Get or create cart for customer"""
        pass
    
    @abstractmethod
    def add_item(self, cart_id: int, item: CartItem) -> CartItem:
        """Add item to cart"""
        pass
    
    @abstractmethod
    def remove_item(self, item_id: int) -> None:
        """Remove item from cart"""
        pass
    
    @abstractmethod
    def get_cart_items(self, cart_id: int) -> list[CartItem]:
        """Get all items in cart"""
        pass
