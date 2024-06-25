
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Product

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'category', 'image', 'excerpt', 'detail', 'price', 'avalible']

class AddStockForm(forms.Form):
    size = forms.IntegerField(label='Talla')
    stock = forms.IntegerField(label='Cantidad de stock')
