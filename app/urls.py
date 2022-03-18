from django.urls import path
from .views import home, contacto, productos

urlpatterns = [
    path('', home, name='home'),
    path('contacto/', contacto, name='contacto'),
    # path('mail/', mail, name='mail'),
    path('productos/', productos, name='productos'),
]
