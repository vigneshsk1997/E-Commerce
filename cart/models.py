from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # For default timestamp

# Product model
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()  # Field to track product stock

    def __str__(self):
        return self.name  # String representation of the product

# Cart model using ManyToMany through CartItem
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Track cart creation time (auto now add)

    def __str__(self):
        return f"Cart {self.id}"

# CartItem model to link Cart and Product
class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)  # Use string to avoid circular import
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def total_price(self):
        """Calculate total price of the cart item"""
        return self.quantity * self.product.price

    def __str__(self):
        """String representation of the cart item"""
        return f"CartItem {self.id} - Product {self.product.name}"
