from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "stock_pcs", "price", "shop", "vip_only")
    list_filter = ("vip_only", "shop")
    search_fields = ("id",)


admin.site.register(Product, ProductAdmin)
