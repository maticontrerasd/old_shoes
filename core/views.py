from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate,login
from django.contrib import messages
from .forms import CustomUserCreationForm,ProductForm,AddStockForm
from .models import Product,ProductStock,Cart, CartItem
from django.db.models import F
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType
from django.conf import settings


#Envio de email

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

#Cambio de contraseña

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm

def home(request):
    return render(request, 'core/home.html')

@login_required
def productos(request):
    products = Product.objects.all()
    return render(request, 'core/productos.html', {"products": products})

def ordenar_productos_por_precio(request):
    products = Product.objects.filter(avalible=True).order_by('price')
    return render(request, 'core/productos.html', {"products": products})

def ordenar_productos_por_precio_desc(request):
    products = Product.objects.filter(avalible=True).order_by('-price')
    return render(request, 'core/productos.html', {"products": products})

def OrdenarPorTallas(request):
    products = Product.objects.all()
    tallas_disponibles = ProductStock.objects.values_list('size', flat=True).distinct()
    selected_talla = request.GET.get('talla')
    if selected_talla:
        products = products.filter(productstock__size=selected_talla)
    return render(request, 'core/productos.html', {"products": products, "tallas_disponibles": tallas_disponibles})

def OrdenarPorMarca(request):
    marca_seleccionada = request.GET.get('marca')
    if marca_seleccionada:
        productos_filtrados = Product.objects.filter(brand=marca_seleccionada)
    else:
        productos_filtrados = Product.objects.all()
    marcas_disponibles = Product.objects.values_list('brand', flat=True).distinct()
    
    context = {
        'products': productos_filtrados,
        'marcas_disponibles': marcas_disponibles,
    }
    return render(request, 'core/productos.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def emailForm(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))


            change_password_url = request.build_absolute_uri(f'/cambiar_contraseña/{uidb64}/{token}/')
            send_mail(
                'Recuperación de Contraseña',
                f'Para cambiar tu contraseña, sigue este enlace: {change_password_url}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )


            return redirect('emailForm_success')
        else:
            return render(request, 'registration/emailForm.html', {'error': 'El correo electrónico no está registrado.'})

    return render(request, 'registration/emailForm.html')

def emailForm_success(request):
    return render(request, 'registration/emailForm_success.html')

def cambiar_contraseña(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('cambio_contraseña_exitoso')
        else:
            form = SetPasswordForm(user)
        return render(request, 'registration/cambiar_contraseña.html', {'form': form})
    else:
        return render(request, 'registration/cambio_contraseña_invalido.html')



def exit(request):
    logout(request)
    return redirect('home')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    stock_por_talla = ProductStock.objects.filter(product=product)
    
    stock_disponible = any(stock_talla.stock > 0 for stock_talla in stock_por_talla)
    
    return render(request, 'core/product_detail.html', {
        'product': product,
        'stock_por_talla': stock_por_talla,
        'stock_disponible': stock_disponible,
    })

def lista_productos(request):
    productos = Product.objects.all()
    context = {'productos': productos}
    return render(request, 'crud/lista_productos.html', context)

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')  
    else:
        form = ProductForm()
    return render(request, 'crud/agregar_producto.html', {'form': form})

def actualizar_producto(request, id):
    producto = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductForm(instance=producto)
    return render(request, 'crud/actualizar_producto.html', {'form': form})

def eliminar_producto(request, id):
    producto = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'crud/eliminar_producto.html', {'producto': producto})

def agregar_stock(request, id):
    producto = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = AddStockForm(request.POST)
        if form.is_valid():
            size = form.cleaned_data['size']
            stock = form.cleaned_data['stock']
            product_stock_entry = ProductStock.objects.filter(product=producto, size=size).first()
            if product_stock_entry:
                ProductStock.objects.filter(product=producto, size=size).update(stock=F('stock') + stock)
            else:
                ProductStock.objects.create(product=producto, size=size, stock=stock)
            return redirect('lista_productos') 
    else:
        form = AddStockForm()
    return render(request, 'crud/agregar_stock.html', {'form': form, 'producto': producto})

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        size = request.POST.get('size')
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        return redirect('cart_detail')
    else:
        return redirect('home')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'carrito/cart_detail.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'El producto ha sido eliminado del carrito.')
    return redirect('cart_detail')

@login_required
def init_transaction(request):
    cart = Cart.objects.get(user=request.user)
    amount = cart.total_price
    buy_order = str(cart.id)  
    session_id = str(request.user.id)
    return_url = request.build_absolute_uri('/payment-confirmation/')

    options = WebpayOptions(
        commerce_code=settings.TRANSBANK_API_KEY,
        api_key=settings.TRANSBANK_SHARED_SECRET,
        integration_type=IntegrationType.TEST
    )

    transaction = Transaction(options)
    response = transaction.create(buy_order, session_id, amount, return_url)

    return redirect(response['url'] + '?token_ws=' + response['token'])

@login_required
def payment_confirmation(request):
    token_ws = request.GET.get('token_ws')

    options = WebpayOptions(
        commerce_code=settings.TRANSBANK_API_KEY,
        api_key=settings.TRANSBANK_SHARED_SECRET,
        integration_type=IntegrationType.TEST
    )

    transaction = Transaction(options)
    response = transaction.commit(token_ws)

    if response['status'] == 'AUTHORIZED':
        cart = Cart.objects.get(user=request.user)
        for cart_item in cart.cartitems.all():
            product_stock = ProductStock.objects.get(product=cart_item.product, size=cart_item.size)
            product_stock.stock -= cart_item.quantity
            product_stock.save()
        cart.delete()
        return render(request, 'carrito/compra_exitosa.html')
    else:
        return render(request, 'carrito/error_compra.html')
    
