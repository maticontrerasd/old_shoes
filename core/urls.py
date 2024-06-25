from django.urls import path
from .views import home,productos,exit, register,product_detail,lista_productos,agregar_producto,actualizar_producto, eliminar_producto,agregar_stock,ordenar_productos_por_precio
from .views import ordenar_productos_por_precio_desc, OrdenarPorTallas, OrdenarPorMarca,add_to_cart, cart_detail,remove_from_cart,init_transaction,payment_confirmation
from .views import emailForm,emailForm_success,cambiar_contraseña
from django.views.generic import TemplateView


urlpatterns = [
    path('',home, name='home'),
    path('productos/', productos, name='productos'),
    path('logout/',exit,name='exit'),
    path('register/',register,name='register'),
    path('emailForm/',emailForm,name='emailForm'),

    path('emailForm_success/',emailForm_success, name='emailForm_success'),
    path('cambiar_contraseña/<str:uidb64>/<str:token>/', cambiar_contraseña, name='cambiar_contraseña'),
    path('cambio_contraseña_exitoso/', TemplateView.as_view(template_name='registration/cambio_contraseña_exitoso.html'), name='cambio_contraseña_exitoso'),

    
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('lista_producto/',lista_productos,name='lista_productos'),
    path('agregar_producto/',agregar_producto,name='agregar_producto'),
    path('actualizar_producto/<int:id>/', actualizar_producto, name='actualizar_producto'),
    path('eliminar_producto/<int:id>/', eliminar_producto, name='eliminar_producto'),
    path('agregar_stock/<int:id>/', agregar_stock, name='agregar_stock'),
    path('ordenar_productos_por_precio/', ordenar_productos_por_precio, name='ordenar_productos_por_precio'),
    path('ordenar_productos_por_precio_desc/', ordenar_productos_por_precio_desc, name='ordenar_productos_por_precio_desc'),
    path('ordenar_por_tallas/', OrdenarPorTallas, name='ordenar_por_tallas'),
    path('ordenar_por_marca/', OrdenarPorMarca, name='ordenar_por_marca'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('init-transaction/', init_transaction, name='init_transaction'),
    path('payment-confirmation/', payment_confirmation, name='payment_confirmation'),
]   
