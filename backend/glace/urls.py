from django.urls import path

from .views import create_order, refill_tub

urlpatterns = [
    path("create-order/", create_order, name="create_order"),
    path("refill-tub/<int:tub_id>/", refill_tub, name="refill_tub"),
]
