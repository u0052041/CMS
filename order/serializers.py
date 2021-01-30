from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    shop = serializers.CharField(required=False)
    customer = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = "__all__"

    def validate(self, data):
        data["shop"] = data.get("product").shop
        data["customer"] = self.context['request'].user
        return data