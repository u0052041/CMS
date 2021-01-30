from CMS.test_setUp import BaseTest
from order.models import Order

from .models import Product


# Create your tests here.
class ProductTest(BaseTest):
    def setUp(self):
        super(ProductTest, self).setUp()

    def test_product(self):
        print("test_product")
        """
            create order first,
            order1: product1 ,qty=100
            order2: product2, qty=40
        """
        self.client.force_login(self.vip_user)
        post_json = {
            "product": self.product1.id,
            "qty": 100,
        }
        self.client.post("/api/order/", post_json)
        post_json = {
            "product": self.product2.id,
            "qty": 40,
        }
        self.client.post("/api/order/", post_json)

        response = self.client.get("/api/product/top3/")
        self.assertEqual(response.status_code, 200)
        assert_json = {
            "top3_product": [
                {"id": self.product1.id, "sales_sum": 100},
                {"id": self.product2.id, "sales_sum": 40},
            ]
        }
        self.assertEqual(response.json(), assert_json)
