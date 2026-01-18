"""Register customer use case"""
from typing import Tuple
from domain.entities.customer import Customer
from interfaces.repositories.customer_repository import CustomerRepository
from django.contrib.auth.hashers import make_password


class RegisterCustomerUseCase:
    """Use case for registering a new customer"""
    
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository
    
    def execute(self, name: str, email: str, password: str) -> Tuple[Customer, str]:
        """
        Register a new customer
        Returns: (Customer, error_message)
        """
        # Check if email already exists
        existing_customer = self.customer_repository.get_by_email(email)
        if existing_customer:
            return None, "Email already exists"
        
        # Validate password
        if len(password) < 6:
            return None, "Password must be at least 6 characters"
        
        # Create customer entity
        password_hash = make_password(password)
        customer = Customer(
            id=None,
            name=name,
            email=email,
            password_hash=password_hash
        )
        
        # Save customer
        created_customer = self.customer_repository.create(customer)
        return created_customer, None
