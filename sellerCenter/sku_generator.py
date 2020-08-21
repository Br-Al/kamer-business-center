from .models import Product, Order
import random, string

def generate_sku(start_string):
	products = Product.objects.all()
	sku_product = products.values('sku')
	start_string = start_string.replace(" ","")[:2]
	
	sku = None
	sku_generator = lambda N: ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for i in range(N)) 
	while {'sku':sku} in sku_product or sku == None:
		sku = start_string.upper() + sku_generator(18)
	return sku

def generate_order_number():
	orders = Order.objects.all()
	order_num = orders.values('order_number')
	num = None
	num_generator = lambda N: ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for i in range(N)) 
	while {'order_number':num} in order_num or num == None:
		num = num_generator(20)
	return num