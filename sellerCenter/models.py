from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .generator import generate_id
from django.db.models.query import QuerySet
from django.utils import timezone
import barcode
from barcode.writer import ImageWriter
from django.core.files.base import ContentFile
from io import BytesIO
# Create your models here.

class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)

class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

class SoftDeletionModel(models.Model):
    deleted_at = models.DateField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()

class City(SoftDeletionModel):
    city_id = models.CharField(db_column='CITY_ID', primary_key=True, max_length=255)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=255)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=128)  # Field name made lowercase.
    created_at = models.DateField(db_column='CREATED_AT', auto_now_add=True)  # Field name made lowercase.


    def set_id(self):
        self.city_id = generate_id('sellerCenter','City','city_id', self.name)

    def __str__(self):
        return self.code

class Product(SoftDeletionModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null = True)
    promo_price = models.PositiveIntegerField(default = 0)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to = 'sellerCenter/product_image/%y/%m/%d')
    sku = models.CharField(max_length=200, primary_key=True)
    barcode = models.ImageField(upload_to = 'sellerCenter/barecode/%y/%m/%d', null = True, blank = True)
    action = models.ManyToManyField(
        User,
        through = 'ProductManagement',
        related_name = 'product'
        
    )

    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    def get_absolute_url(self):
        return 'http://kamerbusinesscenter.com'+ reverse('shop:product.view.shop', args = [self.sku])

    def set_id(self):
        self.sku = generate_id('sellerCenter','Product','sku', self.name)
        code39 = barcode.get('code39', self.sku, writer = ImageWriter())
        code39_img = code39.render()
        image_io = BytesIO()
        code39_img.save(image_io, format='PNG')
        image_name = 'barcode-'+self.sku
        self.barcode.save(image_name, content=ContentFile(image_io.getvalue()), save=False)
        
    def __str__(self):
        return self.name

    delivery_fee = models.ManyToManyField(
        City,
        through='DeliveryFee',
        related_name='delivery_fee'

    )
class Referal(models.Model):
    referal_id = models.CharField(db_column='REFERAL_ID', primary_key=True, max_length=255)  # Field name made lowercase.
    product = models.ForeignKey(Product, models.DO_NOTHING, db_column='SKU')  # Field name made lowercase.
    seller = models.ForeignKey(User, models.DO_NOTHING, db_column='USER_ID')  # Field name made lowercase.
    link = models.CharField(db_column='LINK', max_length=255, null = True)  # Field name made lowercase.
    is_active = models.BooleanField(db_column='IS_ACTIVE', default = True)  # Field name made lowercase.
    
    class Meta:
        db_table = 'referal'

    def set_link(self):
        self.link = 'http://kamerbusinesscenter.com'+ reverse('shop:product.view.shop', args = [self.referal_id])
    
    def set_id(self):
        self.referal_id = generate_id('sellerCenter','Referal','referal_id', 'Referal')

class Order(SoftDeletionModel):
    customer_firstName = models.CharField(max_length=200)
    customer_lastName = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=200)
    customer_email = models.EmailField()
    total_price = models.PositiveIntegerField()
    delivery_fee = models.PositiveIntegerField(default = 0)
    delivery_address = models.CharField(max_length=200, null = True)
    order_number = models.CharField(max_length=200, primary_key=True)
    status = models.CharField(max_length=200, default="Complet")
    payment_status = models.CharField(max_length=200, default="En attente")
    barcode = models.ImageField(upload_to = 'sellerCenter/barecode/%y/%m/%d', null = True, blank = True)
    referal = models.ForeignKey(Referal, models.DO_NOTHING, db_column='REFERAL_ID', null = True)  # Field name made lowercase.
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
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

    def set_id(self):
        self.order_number = generate_id('sellerCenter','Order','order_number', 'ORDER')
        code39 = barcode.get('code39', self.order_number, writer = ImageWriter())
        code39_img = code39.render()
        image_io = BytesIO()
        code39_img.save(image_io, format='PNG')
        image_name = 'barcode-'+self.order_number
        self.barcode.save(image_name, content=ContentFile(image_io.getvalue()), save=False)

class DeliveryFee(SoftDeletionModel):
    city = models.ForeignKey(City, models.DO_NOTHING, db_column='CITY_ID')  # Field name made lowercase.
    sku = models.ForeignKey(Product, models.DO_NOTHING, db_column='SKU')  # Field name made lowercase.
    amount = models.PositiveIntegerField(db_column='AMOUNT', default = 1500)  # Field name made lowercase.
    created_at = models.DateField(db_column='CREATED_AT', auto_now_add=True)  # Field name made lowercase.
   
class OrderProduct(SoftDeletionModel):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

class ProductManagement(SoftDeletionModel):
    action =  models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)

class OrderManagement(SoftDeletionModel):
    action =  models.CharField(max_length=200)
    reason =  models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)


