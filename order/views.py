from django.db.models import F
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "id"


def datatable_order_list(request):
    if not request.is_ajax():
        return Response(status=403)
    draw = request.GET.get("draw")  # 頁數
    length = int(request.GET.get("length"))  # 單頁行數
    start = int(request.GET.get("start"))  # queryset first index

    order = Order.objects.all()
    select_order = order[start : start + length]
    select_order = select_order.annotate(price=F("product__price"))
    json_response = dict()
    json_response["data"] = list(select_order.values("id", "product__id", "qty", "price", "shop__id", "customer__id"))
    json_response["draw"] = draw
    json_response["length"] = length
    json_response["recordsFiltered"] = order.count()
    return JsonResponse(json_response, safe=False)