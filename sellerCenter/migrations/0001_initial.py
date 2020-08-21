# Generated by Django 2.2.7 on 2020-06-20 06:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('customer_firstName', models.CharField(max_length=200)),
                ('customer_lastName', models.CharField(max_length=200)),
                ('customer_phone', models.CharField(max_length=200)),
                ('customer_email', models.EmailField(max_length=254)),
                ('total_price', models.PositiveIntegerField()),
                ('delivery_fee', models.PositiveIntegerField(null=True)),
                ('delivery_address', models.CharField(max_length=200, null=True)),
                ('order_number', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(null=True)),
                ('discount', models.PositiveIntegerField(default=0)),
                ('price', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to='sellerCenter/product_image/%y/%m/%d')),
                ('sku', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductManagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sellerCenter.Product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='action',
            field=models.ManyToManyField(related_name='product', through='sellerCenter.ProductManagement', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellerCenter.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellerCenter.Product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderManagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=200)),
                ('reason', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellerCenter.Order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='action',
            field=models.ManyToManyField(related_name='order', through='sellerCenter.OrderManagement', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='order', through='sellerCenter.OrderProduct', to='sellerCenter.Product'),
        ),
    ]