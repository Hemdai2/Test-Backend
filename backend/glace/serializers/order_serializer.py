from rest_framework import serializers
from glace.models import Order, OrderItem
from glace.serializers import FlavorSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    flavor = FlavorSerializer()

    class Meta:
        model = OrderItem
        fields = ["flavor", "quantity"]


class OrderCreateSerializer(serializers.ModelSerializer):
    scoops = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ["comments", "scoops"]
