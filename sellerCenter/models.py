from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.



class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null = True)
    discount = models.PositiveIntegerField(default = 0)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to = 'sellercenter/product_image/%y/%m/%d')
    sku = models.CharField(max_length=200, primary_key=True)
    action = models.ManyToManyField(
        User,
        through = 'ProductManagement',
        related_name = 'product'
        
    )
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def get_absolute_url(self):
        return 'localhost:8000'+ reverse('shop:product.view.shop', args = [self.sku])

class Order(models.Model):
    customer_firstName = models.CharField(max_length=200)
    customer_lastName = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=200)
    customer_email = models.EmailField()
    total_price = models.PositiveIntegerField()
    delivery_fee = models.PositiveIntegerField(null = True)
    delivery_address = models.CharField(max_length=200, null = True)
    order_number = models.CharField(max_length=200, primary_key=True)
    status = models.CharField(max_length=200, default="pending")
    products = models.ManyToManyField(
        Product,
        through = 'OrderProduct',
        related_name = 'order'
    )
    action = models.ManyToManyField(
        User,
        through = 'OrderManagement',
        related_name = 'order'
    )
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
class ProductManagement(models.Model):
    action =  models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)

class OrderManagement(models.Model):
    action =  models.CharField(max_length=200)
    reason =  models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
