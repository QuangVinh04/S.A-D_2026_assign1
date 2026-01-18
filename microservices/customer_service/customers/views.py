"""Views for Customer API"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Customer
from .serializers import (
    CustomerSerializer,
    CustomerLoginSerializer,
    CustomerResponseSerializer
)


class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Customer CRUD operations
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'login':
            return CustomerLoginSerializer
        elif self.action in ['list', 'retrieve', 'get_by_id']:
            return CustomerResponseSerializer
        return CustomerSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to return consistent format"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(
                {
                    'success': True,
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Customer.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'message': 'Customer not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Register a new customer"""
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            response_serializer = CustomerResponseSerializer(customer)
            return Response(
                {
                    'success': True,
                    'message': 'Customer registered successfully',
                    'data': response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'success': False,
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Login customer"""
        serializer = CustomerLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            customer = Customer.objects.get(email=email)
            if customer.check_password(password):
                response_serializer = CustomerResponseSerializer(customer)
                return Response(
                    {
                        'success': True,
                        'message': 'Login successful',
                        'data': response_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'success': False,
                        'message': 'Invalid email or password'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Customer.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'message': 'Invalid email or password'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    @action(detail=True, methods=['get'])
    def get_by_id(self, request, pk=None):
        """Get customer by ID (alias for retrieve)"""
        return self.retrieve(request, pk=pk)