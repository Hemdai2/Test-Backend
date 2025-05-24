from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Tub, Flavor, Order

from .serializers import (
    OrderCreateSerializer,
    TubSerializer,
    FlavorSerializer,
    OrderItemReadSerializer,
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


@api_view(["POST"])
def refill_tub(request, tub_id):
    try:
        tub = Tub.objects.get(pk=tub_id)
        if not tub.scoops_left < 40:
            return Response(
                {"message": "Le pot est plein, il ne peut pas être rempli"}, status=400
            )

        needed_scoops = tub.capacity - tub.scoops_left

        print(
            f"Tub for {tub.flavor.name} has {tub.scoops_left} left. now adding {needed_scoops} scoops (Email would be sent to admin)"
        )
        tub.refill(needed_scoops)
        response_data = {
            "message": f"Le pot de glace {tub.flavor.name} a été rempli.",
            "data": TubSerializer(tub).data,
        }
        return Response(response_data)

    except Tub.DoesNotExist:
        return Response({"error": "le pot n'existe pas"}, status=404)


@api_view(["GET"])
def get_flavors(request):
    flavors = Flavor.objects.all()
    serializer = FlavorSerializer(flavors, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_order_details(request, order_id):
    try:
        order = Order.objects.get(order_code=order_id)
        serializer = OrderItemReadSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)


@api_view(["GET"])
def get_all_orders(request):
    orders = Order.objects.all()
    serializer = OrderReadSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_all_tubs(request):
    tubs = Tub.objects.all()
    serializer = TubSerializer(tubs, many=True)
    return Response(serializer.data)
