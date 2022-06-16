from unicodedata import name
from django.urls import path
from .views import home, profile, registro, contacto, productos, view_producto, add_prd_cart, del_prd_cart, cart, \
    sub_prd_cart, incr_prd_cart, send_pedido_cart, clean_cart, generate_coupon

urlpatterns = [
    path('', home, name='home'),
    path('signup/', registro, name='registro'),
    path('contacto/', contacto, name='contacto'),
    path('cart/', cart, name='cart'),
    path('clean_cart/', clean_cart, name='clean_cart'),
    path('enviar_pedido/', send_pedido_cart, name='send_pedido_cart'),
    path('generar_coupon/', generate_coupon, name='generate_coupon'),

    # Productos
    path('productos/', productos, name='productos'),
    path('<username>/', profile, name='profile'),
    path('<str:nombre>/<int:id>/', view_producto, name='view_producto'),
    path('add_prd_cart/<str:nombre>/<int:id>/', add_prd_cart, name='add_prd_cart'),
    path('incr_prd_cart/<str:nombre>/<int:id>/', incr_prd_cart, name='incr_prd_cart'),
    path('sub_prd_cart/<str:nombre>/<int:id>/', sub_prd_cart, name='sub_prd_cart'),
    path('del_prd_cart/<str:nombre>/<int:id>/', del_prd_cart, name='del_prd_cart'),
]
