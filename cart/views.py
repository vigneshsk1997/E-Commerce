from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Cart
from products.models import Product

@login_required
def view_cart(request):
    # Get all cart items for the current user
    cart_items = Cart.objects.filter(user=request.user)
    
    # Calculate the total price of all items in the cart
    total_price = sum(item.total_price() for item in cart_items)
    
    # Render the cart template with cart items and total price
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    try:
        # Fetch the product using the product_id
        product = Product.objects.get(id=product_id)
        
        # Check if the user already has this product in their cart
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        
        if not created:
            # If the product already exists, increase the quantity
            cart_item.quantity += 1
            cart_item.save()
        
        # Redirect to the cart view after adding the product
        return redirect('view_cart')
    
    except Product.DoesNotExist:
        # Handle the case where the product does not exist
        raise Http404("Product not found")
