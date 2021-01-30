from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from order.models import Order

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

    @action(methods=["GET"], detail=False, url_path="top3")
    def sales_top3(self, request):
        """
            calc order qty sum in different product
        """
        proudct_top3 = (
            Product.objects.all()
            .annotate(sales_sum=Coalesce(Sum("order__qty"), 0))
            .order_by("-sales_sum")[:3]
        )
        response_json = {"top3_product": list(proudct_top3.values("id", "sales_sum"))}
        return Response(response_json, status=status.HTTP_200_OK)


def datatable_product_list(request):
    if not request.is_ajax():
        return Response(status=403)
    draw = request.GET.get("draw")  # 頁數
    length = int(request.GET.get("length"))  # 單頁行數
    start = int(request.GET.get("start"))  # queryset first index

    product = Product.objects.all().order_by("id")
    select_product = product[start : start + length]

    json_response = dict()
    json_response["data"] = list(
        select_product.values("id", "stock_pcs", "price", "shop__id", "vip_only")
    )
    json_response["draw"] = draw
    json_response["length"] = length
    json_response["recordsFiltered"] = product.count()
    return JsonResponse(json_response, safe=False)
