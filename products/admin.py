from django.contrib import admin
from .models import Product
from cart.models import Cart, CartItem

# Register Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')

# Register Cart model
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_quantity', 'get_total_price')  # Display user, total quantity, and total price

    def get_total_quantity(self, obj):
        return sum(cart_item.quantity for cart_item in obj.cart_items.all())
    get_total_quantity.short_description = 'Total Quantity'

    def get_total_price(self, obj):
        return sum(cart_item.get_total() for cart_item in obj.cart_items.all())
    get_total_price.short_description = 'Total Price'



