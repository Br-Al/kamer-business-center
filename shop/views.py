from django.shortcuts import render, redirect, get_object_or_404
from sellercenter.models import Product, Order, OrderProduct
from sellercenter.sku_generator import generate_order_number
from django.contrib import messages
from django.urls import reverse
# Create your views here.
def shop(request, sku):
	product = get_object_or_404(Product, pk = sku)
	return render(request, 'shop/product.html', {'product':product})

def makeOrder(request, sku):
	reverse('shop:make.order', args = [sku] )
	product = get_object_or_404(Product, pk = sku)
	order = Order()
	params = request.POST
	order.customer_firstName = params.get('customer_firstName')
	order.customer_lastName = params.get('customer_lastName')
	order.customer_phone = params.get('customer_phone')
	order.delivery_address = params.get('delivery_address')
	if params.get('city') == "douala" and order.delivery_address != None:
		order.delivery_fee = 1000
	if params.get('city') == "yaounde" and order.delivery_address != None:
		order.delivery_fee = 1500
	order.order_number = generate_order_number()
	order.customer_email = params.get('customer_email')
	order.total_price = (product.price - product.price*product.discount) * int(params.get('quantity')) + order.delivery_fee
	order.save()
	OrderProduct.objects.create(order = order, product = product, quantity = int(params.get('quantity')))
	#print(order.products.all()[0].name)
	messages.success(request, 'Your order has been registered !')

	return render(request, 'shop/product.html', {'product':product})

