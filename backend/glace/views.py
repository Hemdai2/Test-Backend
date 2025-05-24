from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import OrderCreateSerializer

# Create your views here.


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
