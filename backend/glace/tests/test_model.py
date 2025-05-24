import pytest
from glace.models import Tub, Flavor, Order, OrderItem


@pytest.mark.django_db
def test_flavor_object_creation():
    """Test pour vérifier la création d'un objet Flavor"""
    flavor = Flavor.objects.create(name="Vanilla")
    assert flavor.name == "Vanilla"


@pytest.mark.django_db
def test_tub_object_creation():
    """Test pour vérifier la création d'un objet Tub"""
    flavor = Flavor.objects.create(name="Chocolate")
    tub = Tub.objects.create(flavor=flavor, scoops_left=40)

    assert tub.flavor == flavor
    assert tub.scoops_left == 40


@pytest.mark.django_db
def test_create_order():
    """Test pour vérifier la création d'un objet Order avec plusieurs OrderItem"""
    vanilla = Flavor.objects.create(name="Vanilla")
    chocolate = Flavor.objects.create(name="Chocolate")
    order = Order.objects.create()
    OrderItem.objects.create(order=order, flavor=vanilla, quantity=2)
    OrderItem.objects.create(order=order, flavor=chocolate, quantity=3)
    assert order.total_price() == 10
