from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistrationForm, updateUserForm, createProductForm, updateProductForm, deliveryFeeForm, CreateCityForm
from django.contrib import messages
from django.urls import reverse
from .models import Product, Order, ProductManagement, DeliveryFee, City, Referal
from .admin import OrderResource, ProductResource
#from .sku_generator import generate_sku


# Create your views here.
@login_required()
def index(request):
	labels = []
	data = []
	orders = Order.objects.all()
	products = Product.objects.all()
	users = User.objects.all()
	
	return render(request, 'sellerCenter/index.html',{'users': users, 'products':products, 'orders': orders})

@login_required()
def users(request):
	registration_form = RegistrationForm()
	users = User.objects.all()
	return render(request, 'sellerCenter/users.html', {'users': users})

@login_required()
def products(request):
	
	products = Product.objects.all().order_by('created_at')
	return render(request, 'sellerCenter/products.html', {'products':products})

@login_required()
def orders(request):
	orders = Order.objects.all().order_by('created_at')
	return render(request, 'sellerCenter/orders.html', {'orders': orders})

""" 
	Create, Update and delete User
"""

# Create a super user if not exist

def createsuperuser(request):
	reverse('sellerCenter:user.create.root')
	users = User.objects.all()
	if len(users) == 0:
		user = User.objects.create_superuser('admin', 'admin@kamerbusinesscenter.com', 'pass')
	return redirect('sellerCenter:dashboard')

@login_required()
def createUser(request):
	reverse('sellerCenter:user.create')
	if request.method == 'POST':
	
		registration_form = RegistrationForm(request.POST)
		users = User.objects.all()
		if registration_form.is_valid(): 
			user = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))
			user.last_name = request.POST.get('last_name')
			user.first_name = request.POST.get('first_name')
			user.save()
			messages.success(request, 'User successful created !')
		else:
			messages.error(request, 'Invalid information, please check your form and correct some fields.')
		return render(request, 'sellerCenter/users.html', {'registration_form': registration_form,'users': users})
	
	else:
		registration_form = RegistrationForm()
		return render(request, 'sellerCenter/forms/user/register.html', {'registration_form': registration_form})
	#return render(request, 'sellerCenter/users.html')
	

@login_required()
def updateUser(request, user_id):
	reverse('sellerCenter:user.update', args=[user_id])
	form = updateUserForm()
	if user_id != None:
		user = get_object_or_404(User, pk=user_id)
		form = updateUserForm(request.POST, instance=user)

		if form.is_valid():
			form.save()
			messages.success(request, 'User successful updated !')
		else:
			messages.error(request, 'Invalid information, please check your form and correct some fields.')
	
	return redirect('sellerCenter:users')

@login_required()
def deleteUser(request, user_id):
	reverse('sellerCenter:user.delete', args=[user_id])
	if user_id != None:
		user = get_object_or_404(User, pk=user_id)
		user.delete()
		messages.success(request, 'User successful deleted !')
	return redirect('sellerCenter:users')

@login_required()
def form_updateUser(request, user_id):
	reverse('sellerCenter:user.form.update', args = [user_id])
	user = get_object_or_404(User, pk=user_id)
	form = updateUserForm(instance = user)
	return render(request, 'sellerCenter/forms/user/update.html', {'form': form, 'user_id':user.id})


@login_required()
def form_createUser(request, user_id):
	reverse('sellerCenter:user.form.create')
	registration_form = RegistrationForm()
	return render(request, 'sellerCenter/forms/user/register.html', {'registration_form': registration_form})

@login_required()
def form_deleteUser(request, user_id):
	reverse('sellerCenter:user.form.delete', args = [user_id])
	print(user_id)
	return render(request, 'sellerCenter/forms/user/delete.html', {'user_id': user_id})


""" 
	Product Management
"""
@login_required()
def createProduct(request, user_id=None):
	
	if request.method == 'POST':
		form_data = request.POST.copy()
		form = createProductForm(form_data, request.FILES)
		if form.is_valid():
			product = form.save(commit=False)
			product.set_id()
			product.save()
			ProductManagement.objects.create(user = request.user, product = product, action = "create")
			messages.success(request, 'Product Saved !')
		return redirect('sellerCenter:products')
	else:
		form = createProductForm()
		return render(request, 'sellerCenter/forms/product/create.html', {'form': form})

@login_required()
def updateProduct(request, sku):
	reverse('sellerCenter:product.update', args=[sku])
	product = get_object_or_404(Product, pk=sku)
	form = updateProductForm(request.POST, request.FILES, instance = product)
	if form.is_valid():
		product = form.save()
		ProductManagement.objects.create(user = request.user, product = product, action = "update")
		messages.success(request, 'Product updated !')
	return redirect('sellerCenter:products')

@login_required()
def deleteProduct(request, sku):
	reverse('sellerCenter:product.delete', args=[sku])
	product = get_object_or_404(Product, pk = sku)
	ProductManagement.objects.create(user = request.user, product = product, action = "delete")
	product.delete()
	messages.success(request, 'Product deleted !')
	return redirect('sellerCenter:products')

@login_required()
def form_updateProduct(request, sku):
	reverse('sellerCenter:product.form.update', args = [sku])
	product = get_object_or_404(Product, pk=sku)
	form = updateProductForm(instance = product)
	return render(request, 'sellerCenter/forms/product/update.html', {'form': form, 'product':product})


@login_required()
def form_createProduct(request, user_id):
	reverse('sellerCenter:product.form.create')
	registration_form = RegistrationForm()
	return render(request, 'sellerCenter/forms/product/create.html', {'registration_form': registration_form})

@login_required()
def form_deleteProduct(request, sku):
	reverse('sellerCenter:product.form.delete', args = [sku])
	return render(request, 'sellerCenter/forms/product/delete.html', {'sku': sku})

@login_required()
def detailsOrder(request, id):
	reverse('sellerCenter:order.details', args = [id])
	order = get_object_or_404(Order, pk = id)
	return render(request, 'sellerCenter/order/details.html', {'order': order })

@login_required()
def generateInvoice(request, id):
	reverse('sellerCenter:order.invoice', args = [id])
	order = get_object_or_404(Order, pk = id)
	return render(request, 'sellerCenter/order/invoice.html', {'order': order})


@login_required()
def deliveryFees(request):
	reverse('sellerCenter:delivery_fees')
	delivery_fees = DeliveryFee.objects.all()
	form = deliveryFeeForm()
	return render(request, 'sellerCenter/delivery_fee.html', {'delivery_fees' : delivery_fees, 'form': form})

@login_required()
def createDeliveryFee(request):
	if request.method == "POST":
		form = deliveryFeeForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Delivery Fee added !')
			return redirect('sellerCenter:delivery_fees')

@login_required()
def getDeliveryFee(request, sku, city_id):
	reverse('sellerCenter:delivery_fee.product.city', args = [sku, city_id])
	delivery_fee = DeliveryFee.objects.filter(sku=sku, city_id = city_id).first()
	return JsonResponse({'delivery_fee':delivery_fee.amount})

@login_required()
def updateDeliveryFee(request):
	reverse('sellerCenter:delivery_fee')
	delivery_fees = DeliveryFee.objects.all()
	return(request, 'sellerCenter/delivery_fee')

@login_required()
def cities(request):
	reverse('sellerCenter:cities')
	cities = City.objects.all().order_by('created_at')
	form = CreateCityForm()
	return render(request, 'sellerCenter/cities.html', {'cities':cities, 'form':form})

@login_required()
def createCity(request):
	reverse('sellerCenter:city.create')
	if request.method == 'POST':
		form = CreateCityForm(request.POST)
		if form.is_valid():
			city = form.save(commit = False)
			city.set_id()
			city.save()
			messages.success(request, 'City created !')
			return redirect('sellerCenter:cities')
		else:
			messages.error(request, 'Error in some field !')
			return redirect('sellerCenter:cities')

def export_orders(request, format = 'xls'):
    dataset = OrderResource().export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="orders.xls"'
    return response

@login_required()
def get_referal_link(request, sku):
	reverse('sellerCenter:seller.product.referal', args = [sku])
	# return the referal link for the product and the connected seller
	# and create a referal link if not yet set.
	referal = Referal.objects.filter(seller=request.user, product=sku).first()
	if referal == None:
		
		product = get_object_or_404(Product, pk = sku)
		referal = Referal.objects.create(seller = request.user, product = product)
		referal.set_id()
		referal.set_link()
		referal.save()

	return JsonResponse({'referal_link': referal.link})