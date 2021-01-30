from CMS.test_setUp import BaseTest
from product.models import Product

from .models import Order


# Create your tests here.
class OrderTest(BaseTest):
    def setUp(self):
        super(OrderTest, self).setUp()

    def test_order_create_and_delete(self):
        print("test_order_create_and_delete")
        # test vip user buy
        post_json = {
            "product": self.product1.id,
            "qty": 100,
        }
        self.client.force_login(self.vip_user)
        response = self.client.post("/api/order/", post_json)
        self.assertEqual(response.status_code, 201)

        # test not vip user buy
        self.client.logout()
        self.client.force_login(self.not_vip_user)
        response = self.client.post("/api/order/", post_json)
        self.assertEqual(response.json(), {"error": "user not vip!"})

        """
            test product stock not enough,
            product1 stock_pcs should be 0
        """
        self.assertEqual(Product.objects.get(id=self.product1.id).stock_pcs, 0)
        post_json = {
            "product": self.product1.id,
            "qty": 1,
        }
        self.client.logout()
        self.client.force_login(self.vip_user)
        response = self.client.post("/api/order/", post_json)
        self.assertEqual(response.json(), {"error": "stock not enough!"})

        """
            test order delete,
            product1 stock pcs is 0 now,
            product1 stock pcs should be 100 after order delete,
            api response should response text: product 1 In Stock!
        """
        order = Order.objects.all()[0]
        response = self.client.delete(f"/api/order/{order.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.get(id=self.product1.id).stock_pcs, 100)
        self.assertEqual(response.json(), f"product {self.product1.id} In Stock!")
