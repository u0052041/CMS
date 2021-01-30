from django.db import transaction
from django.db.models import F
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from CMS import decorator
from product.models import Product

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "id"

    @transaction.atomic
    @decorator.check_vip
    @decorator.check_product_is_enough
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        product_obj = Product.objects.select_for_update(nowait=True).get(
            id=request.data.get("product")
        )
        product_obj.stock_pcs -= int(request.data.get("qty"))
        product_obj.save(update_fields=["stock_pcs"])
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """
            destroy order, return text In Stock  if Product stock_pcs from 0 to positive integer
        """
        instance = self.get_object()
        product_id = instance.product.id
        order_qty = instance.qty
        self.perform_destroy(instance)
        product_obj = Product.objects.select_for_update(nowait=True).get(id=product_id)
        product_init_pcs = product_obj.stock_pcs
        product_obj.stock_pcs += order_qty
        product_obj.save(update_fields=["stock_pcs"])
        response_text = (
            f"product {product_id} In Stock!" if product_init_pcs == 0 else ""
        )
        return Response(response_text, status=status.HTTP_200_OK)


def datatable_order_list(request):
    if not request.is_ajax():
        return Response(status=403)
    draw = request.GET.get("draw")  # 頁數
    length = int(request.GET.get("length"))  # 單頁行數
    start = int(request.GET.get("start"))  # queryset first index

    order = Order.objects.all().order_by("id")
    select_order = order[start : start + length]
    select_order = select_order.annotate(price=F("product__price"))
    json_response = dict()
    json_response["data"] = list(
        select_order.values(
            "id", "product__id", "qty", "price", "shop__id", "customer__id"
        )
    )
    json_response["draw"] = draw
    json_response["length"] = length
    json_response["recordsFiltered"] = order.count()
    return JsonResponse(json_response, safe=False)
