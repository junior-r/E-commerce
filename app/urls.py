from django.urls import path
from .views import home, profile, registro, contacto, productos

urlpatterns = [
    path('', home, name='home'),
    path('signup/', registro, name='registro'),
    path('contacto/', contacto, name='contacto'),
    # path('mail/', mail, name='mail'),
    path('productos/', productos, name='productos'),
    path('<username>/', profile, name='profile'),
]
