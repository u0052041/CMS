from rest_framework import status
from rest_framework.response import Response

from product.models import Product


def check_vip(function):
    """
        return http_400 if product is vip only and request.user not vip
    """

    def wrap(viewset, request, *args, **kwargs):
        if not request.data.get("product"):
            return Response(
                {"error": "product can not be None!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            product_obj = Product.objects.get(id=request.data.get("product"))
        except Product.DoesNotExist:
            return Response(
                {"error": "product does not exists!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        product_vip_only = product_obj.vip_only
        is_vip = request.user.userprofile.is_vip
        if product_vip_only and not is_vip:
            return Response(
                {"error": "user not vip!"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return function(viewset, request, *args, **kwargs)

    return wrap


def check_product_is_enough(function):
    """
        check product stock is enough
    """

    def wrap(viewset, request, *args, **kwargs):
        try:
            qty_to_buy = int(request.data.get("qty"))
        except ValueError:
            return Response(
                {"error": "qty must be integer!"}, status=status.HTTP_400_BAD_REQUEST
            )
        product_obj = Product.objects.select_for_update(nowait=True).get(
            id=request.data.get("product")
        )
        if product_obj.stock_pcs < qty_to_buy:
            return Response(
                {"error": "stock not enough!"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return function(viewset, request, *args, **kwargs)

    return wrap
