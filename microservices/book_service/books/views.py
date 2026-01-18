"""Views for Book API"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book CRUD operations
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
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
        except Book.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'message': 'Book not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def catalog(self, request):
        """Get all books (catalog)"""
        books = self.get_queryset()
        serializer = self.get_serializer(books, many=True)
        return Response(
            {
                'success': True,
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'])
    def get_by_id(self, request, pk=None):
        """Get book by ID"""
        return self.retrieve(request, pk=pk)