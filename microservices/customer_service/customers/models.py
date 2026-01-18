"""Customer model for customer-service microservice"""
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Customer(models.Model):
    """Customer model"""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customers'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.email})"

    def set_password(self, raw_password):
        """Set hashed password"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check password"""
        return check_password(raw_password, self.password)
