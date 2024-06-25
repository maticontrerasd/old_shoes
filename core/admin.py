from django.contrib import admin
from .models import Category,Product, ProductStock,Cart,CartItem

# Register your models here.
admin.site.register([Category,Product,ProductStock,Cart,CartItem])