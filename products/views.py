from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product, Cart

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity', 1))  # Quantity should be in POST data
    try:
        Cart.add_to_cart(request.user, product, quantity)
        return redirect('cart_view')
    except ValueError as e:
        return render(request, 'products/product_list.html', {'error': str(e)})

def cart_view(request):
    cart_items = Cart.get_cart_items(request.user)
    total_price = Cart.get_cart_total(request.user)
    return render(request, 'cart_view.html', {'cart_items': cart_items, 'total_price': total_price})

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    Cart.remove_from_cart(request.user, product)
    return redirect('cart_view')

def clear_cart(request):
    Cart.clear_cart(request.user)
    return redirect('cart_view')   #--->file



