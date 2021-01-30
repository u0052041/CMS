from django.db import models
from shop.models import Shop

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    stock_pcs =  models.PositiveIntegerField(default=0, null=False, blank=False)
    price = models.DecimalField(default=0, max_digits=12, decimal_places=2, null=False, blank=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    vip_only = models.BooleanField(default=False)
