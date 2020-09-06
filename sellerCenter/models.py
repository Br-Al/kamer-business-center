from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .generator import generate_id
# Create your models here.


class City(models.Model):
    city_id = models.CharField(db_column='CITY_ID', primary_key=True, max_length=255)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=255)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=128)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='CREATED_AT', auto_now_add=True)  # Field name made lowercase.
    deleted_at = models.DateTimeField(db_column='DELETED_AT', blank=True, null=True)  # Field name made lowercase.


    def set_id(self):
        self.city_id = generate_id('sellerCenter','City','city_id', self.name)

    def __str__(self):
        return self.code

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null = True)
    promo_price = models.PositiveIntegerField(default = 0)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to = 'sellerCenter/product_image/%y/%m/%d')
    sku = models.CharField(max_length=200, primary_key=True)
    action = models.ManyToManyField(
        User,
        through = 'ProductManagement',
        related_name = 'product'
        
    )
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def get_absolute_url(self):
        return 'http://kamerbusinesscenter.com'+ reverse('shop:product.view.shop', args = [self.sku])

    def set_id(self):
        self.sku = generate_id('sellerCenter','Product','sku', self.name)

    def __str__(self):
        return self.name

    delivery_fee = models.ManyToManyField(
        City,
        through='DeliveryFee',
        related_name='delivery_fee'

    )
        
class Order(models.Model):
    customer_firstName = models.CharField(max_length=200)
    customer_lastName = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=200)
    customer_email = models.EmailField()
    total_price = models.PositiveIntegerField()
    delivery_fee = models.PositiveIntegerField(default = 0)
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

    def set_id(self):
        self.order_number = generate_id('sellerCenter','Order','order_number', 'ORDER')



class DeliveryFee(models.Model):
    city = models.ForeignKey(City, models.DO_NOTHING, db_column='CITY_ID')  # Field name made lowercase.
    sku = models.ForeignKey('Product', models.DO_NOTHING, db_column='SKU')  # Field name made lowercase.
    amount = models.PositiveIntegerField(db_column='AMOUNT')  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='CREATED_AT', auto_now_add=True)  # Field name made lowercase.
    deleted_at = models.DateTimeField(db_column='DELETED_AT', blank=True, null=True)  # Field name made lowercase.
   
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
