from django.contrib import admin

from .models import Shop


class ShopAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name",)


admin.site.register(Shop, ShopAdmin)
