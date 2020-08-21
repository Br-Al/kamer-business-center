from django import forms
from django.contrib.auth.models import User
from .models import Product

class RegistrationForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username','email','last_name','first_name','password')
		#fields.widget.attrs.update({'class' : 'form-control'})

		widgets = { 
            'username': forms.TextInput(attrs={'class': 'form-control','id': 'username','placeholder': 'User Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','id': 'inputEmail','placeholder': 'Email'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','id': 'last_name','placeholder': 'Last Name'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','id': 'first_name','placeholder': 'First Name'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control','id': 'password','placeholder': 'Password'}),
        }
class updateUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email','last_name','first_name')
		#fields.widget.attrs.update({'class' : 'form-control'})

		widgets = { 
            'email': forms.EmailInput(attrs={'class': 'form-control','id': 'inputEmail','placeholder': 'Email'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','id': 'last_name','placeholder': 'Last Name'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','id': 'first_name','placeholder': 'First Name'}),
        }

class createProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ('sku','name','description','discount','price','image')

		widgets = { 
            'name': forms.TextInput(attrs={'class': 'form-control','id': 'name','placeholder': 'Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
class updateProductForm(forms.ModelForm):
    image = forms.FileField(required = False, widget = forms.FileInput)
    class Meta:
        model = Product
        fields = ('name','description','discount','price','image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','id': 'name','placeholder': 'Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }