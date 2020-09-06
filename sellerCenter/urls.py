from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from .forms import RegistrationForm

app_name = 'sellerCenter'

urlpatterns = [
   # path('', RedirectView.as_view(url='dashboard')),
    
    path('', RedirectView.as_view(url='dashboard')),
    path('dashboard', views.index, name = "dashboard"),
    path('users', views.users, name = "users"),
    path('products', views.products, name = "products"),
    path('orders', views.orders, name = "orders"),
    path('login', auth_views.LoginView.as_view(), name = "login"),
    path('user', views.createUser, name = "user.create"),
    path('user/update/<int:user_id>', views.updateUser, name = "user.update"),
    path('user/form-update/<int:user_id>', views.form_updateUser, name = "user.form.update"),
    path('user/delete/<int:user_id>', views.deleteUser, name = "user.delete"),
    path('user/form-delete/<int:user_id>', views.form_deleteUser, name = "user.form.delete"),
    path('user/root/create', views.createsuperuser, name = "user.create.root"),
    path('product', views.createProduct, name = "product.create"),
    path('product/<str:sku>', views.createProduct, name = "product.view.shop"),
    path('product/update/<str:sku>', views.updateProduct, name = "product.update"),
    path('product/form-update/<str:sku>', views.form_updateProduct, name = "product.form.update"),
    path('product/delete/<str:sku>', views.deleteProduct, name = "product.delete"),
    path('product/form-delete/<str:sku>', views.form_deleteProduct, name = "product.form.delete"),

    path('order/<str:id>/details', views.detailsOrder, name = 'order.details'),
    path('order/<str:id>/invoice', views.generateInvoice, name ='order.invoice'),

    path('delivery_fees', views.deliveryFees, name = 'delivery_fees'),
    path('delivery_fee/create', views.createDeliveryFee, name = 'delivery_fee.create'),
    path('delivery_fee/<str:sku>/<str:city_id>', views.getDeliveryFee, name = 'delivery_fee.product.city'),
    
    path('cities', views.cities, name = 'cities'),
    path('city/create', views.createCity, name = 'city.create'),
]