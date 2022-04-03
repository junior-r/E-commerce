from unicodedata import name
from django.urls import path
from .views import home, profile, registro, contacto, productos, view_producto

urlpatterns = [
    path('', home, name='home'),
    path('signup/', registro, name='registro'),
    path('contacto/', contacto, name='contacto'),
    # path('mail/', mail, name='mail'),
    path('productos/', productos, name='productos'),
    path('<str:nombre>/<int:id>/', view_producto, name='view_producto'),
    path('<username>/', profile, name='profile'),
]
