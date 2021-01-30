from django.db import models

from shop.models import Shop


# Create your models here.
class ShopDailyReport(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    date = models.DateField(db_index=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    total_order_count = models.PositiveIntegerField(default=0, null=False, blank=False)
    total_order_qty = models.PositiveIntegerField(default=0, null=False, blank=False)
    total_order_amount = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, null=False, blank=False
    )
