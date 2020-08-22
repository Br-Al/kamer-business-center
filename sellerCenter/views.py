from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegistrationForm, updateUserForm, createProductForm, updateProductForm
from django.contrib import messages
from django.urls import reverse
from .models import Product, Order, ProductManagement
from .sku_generator import generate_sku


# Create your views here.
@login_required()
def index(request):
	labels = []
	data = []
	orders = Order.objects.all()
	products = Product.objects.all()
	users = User.objects.all()
	
	return render(request, 'sellercenter/index.html',{'users': users, 'products':products, 'orders': orders})

@login_required()
def users(request):
	registration_form = RegistrationForm()
	users = User.objects.all()
	return render(request, 'sellercenter/users.html', {'users': users})

@login_required()
def products(request):
	
	products = Product.objects.all()
	return render(request, 'sellercenter/products.html', {'products':products})

@login_required()
def orders(request):
	orders = Order.objects.all()
	return render(request, 'sellercenter/orders.html', {'orders': orders})

""" 
	Create, Update and delete User
"""
@login_required()
def createUser(request):
	reverse('sellercenter:user.create')
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
		return render(request, 'sellercenter/users.html', {'registration_form': registration_form,'users': users})
	
	else:
		registration_form = RegistrationForm()
		return render(request, 'sellercenter/forms/user/register.html', {'registration_form': registration_form})
	#return render(request, 'sellercenter/users.html')
	

@login_required()
def updateUser(request, user_id):
	reverse('sellercenter:user.update', args=[user_id])
	form = updateUserForm()
	if user_id != None:
		user = get_object_or_404(User, pk=user_id)
		form = updateUserForm(request.POST, instance=user)

		if form.is_valid():
			form.save()
			messages.success(request, 'User successful updated !')
		else:
			messages.error(request, 'Invalid information, please check your form and correct some fields.')
	
	return redirect('sellercenter:users')

@login_required()
def deleteUser(request, user_id):
	reverse('sellercenter:user.delete', args=[user_id])
	if user_id != None:
		user = get_object_or_404(User, pk=user_id)
		user.delete()
		messages.success(request, 'User successful deleted !')
	return redirect('sellercenter:users')

@login_required()
def form_updateUser(request, user_id):
	reverse('sellercenter:user.form.update', args = [user_id])
	user = get_object_or_404(User, pk=user_id)
	form = updateUserForm(instance = user)
	return render(request, 'sellercenter/forms/user/update.html', {'form': form, 'user_id':user.id})


@login_required()
def form_createUser(request, user_id):
	reverse('sellercenter:user.form.create')
	registration_form = RegistrationForm()
	return render(request, 'sellercenter/forms/user/register.html', {'registration_form': registration_form})

@login_required()
def form_deleteUser(request, user_id):
	reverse('sellercenter:user.form.delete', args = [user_id])
	print(user_id)
	return render(request, 'sellercenter/forms/user/delete.html', {'user_id': user_id})


""" 
	Product Management
"""
@login_required()
def createProduct(request, user_id=None):
	
	if request.method == 'POST':
		form_data = request.POST.copy()
		form_data['sku'] = generate_sku(form_data['name'])
		form = createProductForm(form_data, request.FILES)
		if form.is_valid():
			product = form.save()
			ProductManagement.objects.create(user = request.user, product = product, action = "create")
			messages.success(request, 'Product Saved :!')
		return redirect('sellercenter:products')
	else:
		form = createProductForm()
		return render(request, 'sellercenter/forms/product/create.html', {'form': form})

@login_required()
def updateProduct(request, sku):
	reverse('sellercenter:product.update', args=[sku])
	product = get_object_or_404(Product, pk=sku)
	form = updateProductForm(request.POST, request.FILES, instance = product)
	if form.is_valid():
		product = form.save()
		ProductManagement.objects.create(user = request.user, product = product, action = "update")
		messages.success(request, 'Product updated !')
	return redirect('sellercenter:products')

@login_required()
def deleteProduct(request, sku):
	reverse('sellercenter:product.delete', args=[sku])
	product = get_object_or_404(Product, pk = sku)
	product.delete()
	#ProductManagement.objects.create(user = request.user, product = product, action = "delete")
	messages.success(request, 'Product deleted !')
	return redirect('sellercenter:products')

@login_required()
def form_updateProduct(request, sku):
	reverse('sellercenter:product.form.update', args = [sku])
	product = get_object_or_404(Product, pk=sku)
	form = updateProductForm(instance = product)
	return render(request, 'sellercenter/forms/product/update.html', {'form': form, 'product':product})


@login_required()
def form_createProduct(request, user_id):
	reverse('sellercenter:product.form.create')
	registration_form = RegistrationForm()
	return render(request, 'sellercenter/forms/product/create.html', {'registration_form': registration_form})

@login_required()
def form_deleteProduct(request, sku):
	reverse('sellercenter:product.form.delete', args = [sku])
	return render(request, 'sellercenter/forms/product/delete.html', {'sku': sku})

@login_required()
def detailsOrder(request, id):
	reverse('sellercenter:order.details', args = [id])
	order = get_object_or_404(Order, pk = id)
	return render(request, 'sellercenter/order/details.html', {'order': order })

@login_required()
def generateInvoice(request, id):
	reverse('sellercenter:order.invoice', args = [id])
	order = get_object_or_404(Order, pk = id)
	return render(request, 'sellercenter/order/invoice.html', {'order': order})