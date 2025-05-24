from django.urls import path

from .views import (
    create_order,
    refill_tub,
    get_all_tubs,
    get_all_orders,
    get_flavors,
    get_order_details,
)

urlpatterns = [
    path("create-order/", create_order, name="create_order"),
    path("refill-tub/<int:tub_id>/", refill_tub, name="refill_tub"),
    path("get-all-tubs/", get_all_tubs, name="get_all_tubs"),
    path("get-all-orders/", get_all_orders, name="get_all_orders"),
    path("get-flavors/", get_flavors, name="get_flavors"),
    path(
        "get-order-details/<int:order_id>/", get_order_details, name="get_order_details"
    ),
]
