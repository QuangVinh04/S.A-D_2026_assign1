"""Customer repository interface"""
from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.customer import Customer


class CustomerRepository(ABC):
    """Interface for customer repository"""
    
    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        """Create a new customer"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email"""
        pass
    
    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """Get customer by id"""
        pass
