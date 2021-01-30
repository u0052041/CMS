from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"


def datatable_product_list(request):
    if not request.is_ajax():
        return Response(status=403)
    draw = request.GET.get("draw")  # 頁數
    length = int(request.GET.get("length"))  # 單頁行數
    start = int(request.GET.get("start"))  # queryset first index

    product = Product.objects.all().order_by("id")
    select_product = product[start : start + length]
    
    json_response = dict()
    json_response["data"] = list(select_product.values("id", "stock_pcs", "price", "shop__id", "vip_only"))
    json_response["draw"] = draw
    json_response["length"] = length
    json_response["recordsFiltered"] = product.count()
    return JsonResponse(json_response, safe=False)