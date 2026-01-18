"""Add to cart use case"""
from typing import Tuple
from domain.entities.cart import CartItem
from interfaces.repositories.cart_repository import CartRepository
from interfaces.repositories.book_repository import BookRepository


class AddToCartUseCase:
    """Use case for adding item to cart"""
    
    def __init__(self, cart_repository: CartRepository, book_repository: BookRepository):
        self.cart_repository = cart_repository
        self.book_repository = book_repository
    
    def execute(self, customer_id: int, book_id: int, quantity: int = 1) -> Tuple[CartItem, str]:
        """
        Add item to cart
        Returns: (CartItem, error_message)
        """
        # Get book
        book = self.book_repository.get_by_id(book_id)
        if not book:
            return None, "Book not found"
        
        # Check stock
        if book.stock <= 0:
            return None, "Book is out of stock"
        
        # Get or create cart
        cart = self.cart_repository.get_or_create_cart(customer_id)
        
        # Create cart item
        cart_item = CartItem(
            id=None,
            book_id=book_id,
            quantity=quantity,
            book_title=book.title,
            book_price=float(book.price)
        )
        
        # Add item to cart
        created_item = self.cart_repository.add_item(cart.id, cart_item)
        return created_item, None
