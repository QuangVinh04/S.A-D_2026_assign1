"""Book model for book-service microservice"""
from django.db import models
from decimal import Decimal


class Book(models.Model):
    """Book model"""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)


    class Meta:
        db_table = 'books'
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def is_available(self):
        """Check if book is in stock"""
        return self.stock > 0
