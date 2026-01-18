"""Django models for database persistence"""
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class CustomerModel(models.Model):
    """Django model for Customer"""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'customers'
    
    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class BookModel(models.Model):
    """Django model for Book"""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    class Meta:
        db_table = 'books'
    
    def __str__(self):
        return self.title


class CartModel(models.Model):
    """Django model for Cart"""
    customer = models.OneToOneField(CustomerModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'carts'


class CartItemModel(models.Model):
    """Django model for CartItem"""
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'cart_items'
