"""Serializers for Customer API"""
from rest_framework import serializers
from .models import Customer
from django.contrib.auth.hashers import make_password


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model"""
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'password', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create customer with hashed password"""
        password = validated_data.pop('password')
        customer = Customer.objects.create(**validated_data)
        customer.set_password(password)
        customer.save()
        return customer
    
    def validate_email(self, value):
        """Validate unique email"""
        if Customer.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value


class CustomerLoginSerializer(serializers.Serializer):
    """Serializer for customer login"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class CustomerResponseSerializer(serializers.ModelSerializer):
    """Serializer for customer response (without password)"""
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
