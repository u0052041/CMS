from django.db import models
from shop.models import Shop
from product.models import Product
from django.contrib.auth.models import User

# Create your models here.
class Order(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0, null=False, blank=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
