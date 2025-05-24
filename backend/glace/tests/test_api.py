import pytest
from rest_framework.test import APIClient
from .factories import FlavorFactory, TubFactory
from ..serializers import FlavorSerializer
from ..models import Flavor, Tub


@pytest.mark.django_db
def test_out_of_stock_flavor():
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
