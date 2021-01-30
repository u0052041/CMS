from django.contrib import admin

from .models import ShopDailyReport


class ShopDailyReportAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "shop",
        "total_order_count",
        "total_order_qty",
        "total_order_amount",
    )
    list_filter = (
        "date",
        "shop",
    )


admin.site.register(ShopDailyReport, ShopDailyReportAdmin)
