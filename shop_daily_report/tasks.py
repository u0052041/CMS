from decimal import Decimal

from celery.schedules import crontab
from celery.task import periodic_task
from django.db.models import Aggregate, Count, DecimalField, F, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

from shop.models import Shop

from .models import ShopDailyReport


@periodic_task(ignore_result=True, run_every=crontab(minute=0, hour=0))
def daily_report():
    shop_query = Shop.objects.all().annotate(
        total_order_count=Coalesce(Count("order"), 0),
        total_order_qty=Coalesce(Sum("order__qty"), 0),
        total_order_amount=Coalesce(
            Sum(
                F("order__product__price") * F("order__qty"),
                output_field=DecimalField(),
            ),
            0,
        ),
    )

    yesterday = timezone.now() - timezone.timedelta(days=1)
    for shop in shop_query:
        ShopDailyReport.objects.create(
            date=yesterday,
            shop=shop,
            total_order_count=shop.total_order_count,
            total_order_qty=shop.total_order_qty,
            total_order_amount=shop.total_order_amount,
        )
