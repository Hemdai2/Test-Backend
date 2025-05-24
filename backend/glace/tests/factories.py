import factory
from ..models import Flavor, Tub, Order, OrderItem


class FlavorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Flavor

    name = factory.Sequence(lambda n: f"Flavor {n}")
    price = 2.00


class TubFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tub

    flavor = factory.SubFactory(FlavorFactory)
    capacity = 40
    scoops_left = 40


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    comments = "Test order"


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    flavor = factory.SubFactory(FlavorFactory)
    quantity = 1
