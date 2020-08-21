from django.urls import path, include
from . import views
from django.views.generic import RedirectView

app_name = 'shop'

urlpatterns = [
   # path('', RedirectView.as_view(url='dashboard')),
    
    path('', RedirectView.as_view(url='dashboard')),
    path('product/<str:sku>', views.shop, name = "product.view.shop"),
    path('product/<str:sku>/order', views.makeOrder, name = "make.order"),

]