"""Cart models for cart-service microservice"""
from django.db import models


class Cart(models.Model):
    """Cart model - stores customer_id reference (not FK since customer is in another service)"""
    customer_id = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Cart for customer {self.customer_id}"


class CartItem(models.Model):
    """CartItem model - stores book_id reference (not FK since book is in another service)"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book_id = models.IntegerField()  # Reference to book in book-service
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart', 'book_id']
    
    def __str__(self):
        return f"CartItem: Book {self.book_id} x {self.quantity}"
