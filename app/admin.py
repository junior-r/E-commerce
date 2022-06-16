from re import search
from django.contrib import admin
from .models import Marca, Talla, Producto, Coupon
from .forms import CouponForm


class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "precio", 'marca', 'fecha_fabricacion']
    search_fields = ["nombre"]
    list_filter = ["marca", "fecha_fabricacion"]
    list_per_page = 10


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'valid_from', 'valid_to', 'active']
    search_fields = ['code']
    list_filter = ['valid_from', 'valid_to', 'active']
    list_per_page = 10


admin.site.register(Marca)
admin.site.register(Talla)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Coupon, CouponAdmin)
