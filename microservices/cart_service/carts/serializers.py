"""Serializers for Cart API"""
from rest_framework import serializers
from .models import Cart, CartItem
from cart_service.services import BookServiceClient


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for CartItem"""
    book_info = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'book_id', 'quantity', 'book_info', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_book_info(self, obj):
        """Get book info from book-service"""
        book_client = BookServiceClient()
        book = book_client.get_book(obj.book_id)
        if book:
            return {
                'id': book.get('id'),
                'title': book.get('title'),
                'author': book.get('author'),
                'price': str(book.get('price')),
            }
        return {
            'id': obj.book_id,
            'title': 'Unknown Book',
            'error': 'Book service unavailable'
        }


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart"""
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'customer_id', 'items', 'total', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total(self, obj):
        """Calculate total from book prices"""
        book_client = BookServiceClient()
        total = 0
        for item in obj.items.all():
            book = book_client.get_book(item.book_id)
            if book:
                price = float(book.get('price', 0))
                total += price * item.quantity
        return total


class AddToCartSerializer(serializers.Serializer):
    """Serializer for adding item to cart"""
    book_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(default=1, min_value=1)