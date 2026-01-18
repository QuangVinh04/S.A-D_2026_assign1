"""Cart repository implementation using Django ORM"""
from typing import Optional
from domain.entities.cart import Cart, CartItem
from interfaces.repositories.cart_repository import CartRepository
from infrastructure.database.models import CartModel, CartItemModel, BookModel


class DjangoCartRepository(CartRepository):
    """Django ORM implementation of CartRepository"""
    
    def get_or_create_cart(self, customer_id: int) -> Cart:
        """Get or create cart for customer"""
        from infrastructure.database.models import CustomerModel
        
        customer_model = CustomerModel.objects.get(id=customer_id)
        cart_model, _ = CartModel.objects.get_or_create(customer=customer_model)
        
        # Load cart items
        items = []
        for item_model in cart_model.items.all():
            items.append(self._cart_item_to_domain(item_model))
        
        return Cart(
            id=cart_model.id,
            customer_id=customer_id,
            items=items,
            created_at=cart_model.created_at
        )
    
    def add_item(self, cart_id: int, item: CartItem) -> CartItem:
        """Add item to cart"""
        cart_model = CartModel.objects.get(id=cart_id)
        book_model = BookModel.objects.get(id=item.book_id)
        
        # Check if item already exists
        existing_item = CartItemModel.objects.filter(
            cart=cart_model,
            book=book_model
        ).first()
        
        if existing_item:
            existing_item.quantity += item.quantity
            existing_item.save()
            return self._cart_item_to_domain(existing_item)
        else:
            cart_item_model = CartItemModel(
                cart=cart_model,
                book=book_model,
                quantity=item.quantity
            )
            cart_item_model.save()
            return self._cart_item_to_domain(cart_item_model)
    
    def remove_item(self, item_id: int) -> None:
        """Remove item from cart"""
        CartItemModel.objects.filter(id=item_id).delete()
    
    def get_cart_items(self, cart_id: int) -> list[CartItem]:
        """Get all items in cart"""
        cart_model = CartModel.objects.get(id=cart_id)
        items = []
        for item_model in cart_model.items.all():
            items.append(self._cart_item_to_domain(item_model))
        return items
    
    def _cart_item_to_domain(self, model: CartItemModel) -> CartItem:
        """Convert Django model to domain entity"""
        return CartItem(
            id=model.id,
            book_id=model.book.id,
            quantity=model.quantity,
            book_title=model.book.title,
            book_price=float(model.book.price)
        )
