from django.db import models

# Create your models here.

class Shop(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(blank=False, null=False, max_length=45)