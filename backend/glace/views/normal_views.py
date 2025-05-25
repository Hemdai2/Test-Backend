from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from glace.models import Tub, Flavor, Order

from glace.serializers import (
    OrderCreateSerializer,
    TubSerializer,
    FlavorSerializer,
    OrderReadSerializer,
)

# Create your views here.


@swagger_auto_schema(
    method="post",
    request_body=OrderCreateSerializer,
    responses={
        201: openapi.Response("Order Created", OrderCreateSerializer),
        400: "Validation Error",
    },
)
@api_view(["POST"])
def create_order(request):
    serializer = OrderCreateSerializer(data=request.data)

    if serializer.is_valid():
        try:
            order = serializer.save()
            return Response(
                {
                    "order_code": order.order_code,
                    "total_price": sum(i.price() for i in order.scoops.all()),
                },
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_flavors(request):
    """
    Récupérer tous les parfums de crème de glace
    """
    flavors = Flavor.objects.all()
    serializer = FlavorSerializer(flavors, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_order_details(request, uniqie_id):
    """
    Récupérer les details d'une commande
    """
    try:
        order = Order.objects.get(order_code=uniqie_id)
        serializer = OrderReadSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)


@api_view(["GET"])
def get_all_orders(request):
    """
    Récupérer toutes les commandes
    """
    orders = Order.objects.all()
    serializer = OrderReadSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_all_tubs(request):
    """
    Récupérer tous les pots
    """
    tubs = Tub.objects.all()
    serializer = TubSerializer(tubs, many=True)
    return Response(serializer.data)
