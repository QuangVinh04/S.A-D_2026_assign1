"""Customer repository implementation using Django ORM"""
from typing import Optional
from domain.entities.customer import Customer
from interfaces.repositories.customer_repository import CustomerRepository
from infrastructure.database.models import CustomerModel


class DjangoCustomerRepository(CustomerRepository):
    """Django ORM implementation of CustomerRepository"""
    
    def create(self, customer: Customer) -> Customer:
        """Create a new customer"""
        customer_model = CustomerModel(
            name=customer.name,
            email=customer.email,
            password=customer.password_hash
        )
        customer_model.save()
        return self._to_domain(customer_model)
    
    def get_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email"""
        try:
            customer_model = CustomerModel.objects.get(email=email)
            return self._to_domain(customer_model)
        except CustomerModel.DoesNotExist:
            return None
    
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """Get customer by id"""
        try:
            customer_model = CustomerModel.objects.get(id=customer_id)
            return self._to_domain(customer_model)
        except CustomerModel.DoesNotExist:
            return None
    
    def _to_domain(self, model: CustomerModel) -> Customer:
        """Convert Django model to domain entity"""
        return Customer(
            id=model.id,
            name=model.name,
            email=model.email,
            password_hash=model.password
        )
