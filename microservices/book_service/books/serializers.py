"""Serializers for Book API"""
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model"""
    is_available = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'stock', 'is_available']
        read_only_fields = ['id']
