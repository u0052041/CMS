from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.test.client import RequestFactory

from product.models import Product
from shop.models import Shop


# Create your tests here.
class BaseTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.vip_user = User.objects.create(username="vip_user", password="testabcd")
        self.vip_user.userprofile.is_vip = True
        self.vip_user.userprofile.save(update_fields=["is_vip"])

        self.not_vip_user = User.objects.create(
            username="not_vip_user", password="testabcd"
        )
        self.not_vip_user.userprofile.is_vip = False
        self.not_vip_user.userprofile.save(update_fields=["is_vip"])

        # create shop
        self.shop1 = Shop.objects.create(name="shop1")
        self.shop2 = Shop.objects.create(name="shop2")

        # vip only product in shop1
        self.product1 = Product.objects.create(
            stock_pcs=100, vip_only=True, price=10, shop=self.shop1
        )
        # product in shop2
        self.product2 = Product.objects.create(
            stock_pcs=100, vip_only=False, price=100, shop=self.shop2
        )
