from CMS.test_setUp import BaseTest
from order.models import Order
from product.models import Product

from .models import ShopDailyReport
from .tasks import daily_report


# Create your tests here.
class ShopDailyReportTest(BaseTest):
    def setUp(self):
        super(ShopDailyReportTest, self).setUp()

    def test_daily_report(self):
        """
            create order first,
            order1: product1 ,qty=100, price=10
            order2: product2, qty=40, price=100
            shop1:
                total_order_count = 1
                total_order_qty = 100
                total_order_amount = 1000
            shop2:
                total_order_count = 1
                total_order_qty = 40
                total_order_amount = 4000
        """
        print("test_daily_report")
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

        daily_report()
        shop1_report = ShopDailyReport.objects.get(shop=self.shop1)
        shop2_report = ShopDailyReport.objects.get(shop=self.shop2)
        self.assertEqual(shop1_report.total_order_count, 1)
        self.assertEqual(shop1_report.total_order_qty, 100)
        self.assertEqual(shop1_report.total_order_amount, 1000)
        self.assertEqual(shop2_report.total_order_count, 1)
        self.assertEqual(shop2_report.total_order_qty, 40)
        self.assertEqual(shop2_report.total_order_amount, 4000)
