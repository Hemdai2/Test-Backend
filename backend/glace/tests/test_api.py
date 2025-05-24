import pytest
from rest_framework.test import APIClient
from .factories import FlavorFactory, TubFactory
from ..serializers import FlavorSerializer
from ..models import Flavor, Tub


@pytest.mark.django_db
def test_out_of_stock_flavor():
    """
    Test pour errorer si le nombre de boules est insuffisant
    """
    client = APIClient()
    flavor = FlavorFactory(name="Cherry")
    Tub.objects.create(flavor=flavor, scoops_left=1)

    order_data = {
        "comments": "Test",
        "scoops": [{"flavor": flavor.id, "quantity": 2}],
    }

    response = client.post(
        "/api/glace/create-order/", data=order_data, content_type="application/json"
    )
    assert response.status_code == 400
    print(response.json(), "response.json()")
    assert (
        "Il ne reste plus assez de boules pour Cherry. Il ne reste que 1."
        in response.json()["error"]
    )


@pytest.mark.django_db
def test_order_creation_success():
    """Test pour vérifier la création d'un objet Order Success"""
    client = APIClient()
    flavor = FlavorFactory(name="Chocolate")
    TubFactory(flavor=flavor)

    order_data = {"comments": "Test", "scoops": [{"flavor": flavor.id, "quantity": 2}]}

    response = client.post(
        "/api/glace/create-order/", data=order_data, content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json()["total_price"] == 4


@pytest.mark.django_db
def test_order_creation_with_mix_flavors_success():
    "Test pour créer un order avec plusieurs types de boules"
    client = APIClient()
    chocolate = FlavorFactory(name="Chocolate")
    vanilla = FlavorFactory(name="Vanilla")
    TubFactory(flavor=chocolate)
    TubFactory(flavor=vanilla)

    order_data = {
        "comments": "Test",
        "scoops": [
            {"flavor": chocolate.id, "quantity": 2},
            {"flavor": vanilla.id, "quantity": 2},
        ],
    }

    response = client.post(
        "/api/glace/create-order/", data=order_data, content_type="application/json"
    )
    assert response.status_code == 201
    assert response.json()["total_price"] == 8


@pytest.mark.django_db
def test_order_creation_with_mix_flavors_one_stock_out_fail():
    "Test pour créer un order avec plusieurs types de boules et un stockage insuffisant"
    client = APIClient()
    chocolate = FlavorFactory(name="Chocolate")
    vanilla = FlavorFactory(name="Vanilla")
    TubFactory(flavor=chocolate)
    TubFactory(flavor=vanilla, scoops_left=5)

    order_data = {
        "comments": "Test",
        "scoops": [
            {"flavor": chocolate.id, "quantity": 2},
            {"flavor": vanilla.id, "quantity": 6},
        ],
    }

    response = client.post(
        "/api/glace/create-order/", data=order_data, content_type="application/json"
    )
    print(response.json())
    assert response.status_code == 400
    print(response.json(), "response.json()")
    assert (
        response.json()["error"]
        == "Il ne reste plus assez de boules pour Vanilla. Il ne reste que 5."
    )


@pytest.mark.django_db
def test_refil_tub_success():
    client = APIClient()
    cherry = FlavorFactory(name="Cherry")
    TubFactory(flavor=cherry, scoops_left=5)
    response = client.post(
        f"/api/glace/refill-tub/{cherry.id}/",
        content_type="application/json",
    )
    response_data = {
        "message": "Le pot de glace Cherry a été rempli.",
        "data": {
            "id": 7,
            "flavor": {"id": 7, "name": "Cherry", "price": "2.00"},
            "scoops_left": 40,
        },
    }
    assert response.status_code == 200

    assert response.json() == response_data


@pytest.mark.django_db
def test_refil_fail_on_full_of_stock():
    client = APIClient()
    cherry = FlavorFactory(name="Cherry")
    TubFactory(flavor=cherry, scoops_left=40)
    response = client.post(
        f"/api/glace/refill-tub/{cherry.id}/",
        content_type="application/json",
    )
    response_data = {
        "message": "Le pot est plein, il ne peut pas être rempli",
    }
    print(response.json())
    assert response.status_code == 400

    assert response.json() == response_data
