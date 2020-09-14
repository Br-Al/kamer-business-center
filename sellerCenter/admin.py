from django.contrib import admin

# Register your models here.
from import_export import resources
from .models import Order, Product

class OrderResource(resources.ModelResource):

    class Meta:
        model = Order

class ProductResource(resources.ModelResource):
    
    class Meta:
        model = Product
