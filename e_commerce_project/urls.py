from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Home view function
def home(request):
    return HttpResponse("Welcome to the E-Commerce site!")

urlpatterns = [
    path('', home),  # This will handle the root URL
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),  # Assuming you have a products app
    path('cart/', include('cart.urls')),  # Include cart URLs
]



