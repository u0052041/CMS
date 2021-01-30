from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "qty", "shop", "customer")
    list_filter = ("product", "shop", "customer")
    search_fields = ("id",)


admin.site.register(Order, OrderAdmin)
