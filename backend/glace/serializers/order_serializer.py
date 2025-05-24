from rest_framework import serializers
from glace.models import Order, OrderItem, Flavor
from glace.serializers import FlavorSerializer


class OrderItemReadSerializer(serializers.ModelSerializer):
    flavor = FlavorSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["flavor", "quantity"]


class OrderItemCreateSerializer(serializers.ModelSerializer):
    flavor = serializers.PrimaryKeyRelatedField(queryset=Flavor.objects.all())

    class Meta:
        model = OrderItem
        fields = ["flavor", "quantity"]


class OrderCreateSerializer(serializers.ModelSerializer):
    scoops = OrderItemCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ["comments", "scoops"]

    def create(self, validated_data):
        items_data = validated_data.pop("scoops")
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            flavor = item_data["flavor"]
            quantity = item_data["quantity"]

            tub = flavor.tub

            # Décrémenter le nombre de boules disponibles
            tub.consume_scoops(quantity)

            OrderItem.objects.create(order=order, flavor=flavor, quantity=quantity)

        return order
