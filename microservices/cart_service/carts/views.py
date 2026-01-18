"""Views for Cart API"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    AddToCartSerializer
)
from cart_service.services import BookServiceClient, CustomerServiceClient


class CartViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Cart operations
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'], url_path='customer/(?P<customer_id>[^/.]+)')
    def get_by_customer(self, request, customer_id=None):
        """Get cart by customer ID"""
        # Validate customer exists
        customer_client = CustomerServiceClient()
        if not customer_client.validate_customer(customer_id):
            return Response(
                {
                    'success': False,
                    'message': 'Customer not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        cart, created = Cart.objects.get_or_create(customer_id=customer_id)
        serializer = self.get_serializer(cart)
        return Response(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'], url_path='customer/(?P<customer_id>[^/.]+)/add')
    def add_item(self, request, customer_id=None):
        """Add item to cart"""
        # Validate customer
        customer_client = CustomerServiceClient()
        if not customer_client.validate_customer(customer_id):
            return Response(
                {
                    'success': False,
                    'message': 'Customer not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book_id = serializer.validated_data['book_id']
        quantity = serializer.validated_data['quantity']
        
        # Validate book exists and check stock
        book_client = BookServiceClient()
        book = book_client.get_book(book_id)
        if not book:
            return Response(
                {
                    'success': False,
                    'message': 'Book not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check stock availability
        if book.get('stock', 0) < quantity:
            return Response(
                {
                    'success': False,
                    'message': f'Insufficient stock. Available: {book.get("stock", 0)}'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create cart
        cart, _ = Cart.objects.get_or_create(customer_id=customer_id)
        
        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book_id=book_id,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Check if new total quantity exceeds stock
            new_quantity = cart_item.quantity + quantity
            if book.get('stock', 0) < new_quantity:
                return Response(
                    {
                        'success': False,
                        'message': f'Cannot add more items. Stock limit exceeded.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = new_quantity
            cart_item.save()
        
        item_serializer = CartItemSerializer(cart_item)
        return Response(
            {
                'success': True,
                'message': 'Item added to cart',
                'data': item_serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['delete'], url_path='item/(?P<item_id>[^/.]+)')
    def remove_item(self, request, item_id=None):
        """Remove item from cart"""
        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.delete()
            return Response(
                {
                    'success': True,
                    'message': 'Item removed from cart'
                },
                status=status.HTTP_200_OK
            )
        except CartItem.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'message': 'Cart item not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )