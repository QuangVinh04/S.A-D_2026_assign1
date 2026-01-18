"""Book Service API Client"""
import requests
from django.conf import settings


class BookServiceClient:
    """Client to communicate with Book Service"""
    
    def __init__(self):
        self.base_url = getattr(settings, 'BOOK_SERVICE_URL', 'http://localhost:8002/api/v1')
        self.timeout = 5  # seconds
    
    def get_book(self, book_id):
        """Get book by ID"""
        try:
            response = requests.get(
                f'{self.base_url}/books/{book_id}/',
                timeout=self.timeout
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data.get('data')
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error calling book service: {e}")
            return None
    
    def get_book_catalog(self):
        """Get all books"""
        try:
            response = requests.get(
                f'{self.base_url}/books/catalog/',
                timeout=self.timeout
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data.get('data', [])
            return []
        except requests.exceptions.RequestException as e:
            print(f"Error calling book service: {e}")
            return []