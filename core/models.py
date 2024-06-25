from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

    class Meta:
        db_table = 'categories'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['-id']

class Product(models.Model):
    name= models.CharField(max_length=200)
    brand = models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/', blank=True)
    excerpt = models.TextField(max_length=300,verbose_name='Extracto')
    detail = models.TextField(max_length=500,verbose_name='Informacion del producto')
    price = models.IntegerField()
    avalible = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta: 
        db_table = 'products'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-id']

class ProductStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.IntegerField()
    stock = models.IntegerField()
        
    def __str__(self):
        return f"{self.product.name} - Talla {self.size}"
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.cartitems.all())

    class Meta:
        db_table = 'carts'
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'
        ordering = ['-created_at']

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cartitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity} unidades"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        db_table = 'cart_items'
        verbose_name = 'Elemento del Carrito'
        verbose_name_plural = 'Elementos del Carrito'
        ordering = ['-id']
    