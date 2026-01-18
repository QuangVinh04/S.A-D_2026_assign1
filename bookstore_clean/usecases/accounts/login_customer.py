"""Login customer use case"""
from typing import Tuple, Optional
from domain.entities.customer import Customer
from interfaces.repositories.customer_repository import CustomerRepository
from django.contrib.auth.hashers import check_password


class LoginCustomerUseCase:
    """Use case for customer login"""
    
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository
    
    def execute(self, email: str, password: str) -> Tuple[Optional[Customer], str]:
        """
        Login customer
        Returns: (Customer, error_message)
        """
        # Get customer by email
        customer = self.customer_repository.get_by_email(email)
        if not customer:
            return None, "Invalid email or password"
        
        # Check password
        if not check_password(password, customer.password_hash):
            return None, "Invalid email or password"
        
        return customer, None
