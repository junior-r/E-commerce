from re import search
from django.contrib import admin
from .models import Marca, Producto

# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "precio", 'marca', 'fecha_fabricacion']
    search_fields = ["nombre"]
    list_filter = ["marca", "fecha_fabricacion"]
    list_per_page = 10

admin.site.register(Marca)
admin.site.register(Producto, ProductoAdmin)
