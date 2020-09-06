from django.shortcuts import render, redirect, get_object_or_404
from sellerCenter.models import Product, Order, OrderProduct, City, DeliveryFee
#from sellerCenter.sku_generator import generate_order_number
from django.contrib import messages
from django.urls import reverse
# Create your views here.
def shop(request, sku):
	product = get_object_or_404(Product, pk = sku)
	cities = City.objects.all()
	return render(request, 'shop/product.html', {'product':product, 'cities':cities})

def makeOrder(request, sku):
	reverse('shop:make.order', args = [sku] )
	product = get_object_or_404(Product, pk = sku)
	order = Order()
	order.set_id()
	params = request.POST
	order.customer_firstName = params.get('customer_firstName')
	order.customer_lastName = params.get('customer_lastName')
	order.customer_phone = params.get('customer_phone')
	
	if params.get('city') != "None":
		city = get_object_or_404(City, pk = params.get('city'))
		order.delivery_fee = DeliveryFee.objects.filter(sku=sku, city_id = city.city_id).first().amount
		order.delivery_address = params.get('delivery_address')
	
	order.customer_email = params.get('customer_email')
	order.total_price = product.promo_price * int(params.get('quantity')) + order.delivery_fee
	order.save()
	OrderProduct.objects.create(order = order, product = product, quantity = int(params.get('quantity')))
	#print(order.products.all()[0].name)
	messages.success(request, 'Your order has been registered !')
	return redirect('shop:thanks')

def thanks(request):
	reverse('shop:thanks')
	return render(request,'shop/thanks.html')
