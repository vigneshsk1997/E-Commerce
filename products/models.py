from django.db import models
from django.contrib.auth.models import User

# Define Product model first
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()  # Field to track product stock

    def __str__(self):
        return self.name  # String representation of the product

# Cart model using ManyToMany through CartItem
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    products = models.ManyToManyField(Product, through='CartItem')  # Use 'Product' as a string to avoid circular import
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def add_to_cart(self, product, quantity):
        """
        Add a product to the cart.
        """
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

    def get_total(self):
        """
        Get the total price of the items in the cart.
        """
        return sum(item.get_total() for item in self.cart_items.all())

    def remove_from_cart(self, product):
        """
        Remove a product from the cart.
        """
        CartItem.objects.filter(cart=self, product=product).delete()

# CartItem model to link Cart and Product
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Use 'Product' directly here
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total(self):
        """
        Get the total price of this cart item (product price * quantity).
        """
        return self.product.price * self.quantity
