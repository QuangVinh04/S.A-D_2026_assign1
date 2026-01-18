"""Customer Service API Client"""
import requests
from django.conf import settings


class CustomerServiceClient:
    """Client to communicate with Customer Service"""
    
    def __init__(self):
        self.base_url = getattr(settings, 'CUSTOMER_SERVICE_URL', 'http://localhost:8001/api/v1')
        self.timeout = 5  # seconds
    
    def get_customer(self, customer_id):
        """Get customer by ID"""
        try:
            response = requests.get(
                f'{self.base_url}/customers/{customer_id}/',
                timeout=self.timeout
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data.get('data')
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error calling customer service: {e}")
            return None
    
    def validate_customer(self, customer_id):
        """Validate if customer exists"""
        customer = self.get_customer(customer_id)
        return customer is not None