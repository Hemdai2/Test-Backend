from rest_framework import serializers
from glace.models import Tub, Flavor
from glace.serializers.flavor_serializer import FlavorSerializer


class TubSerializer(serializers.ModelSerializer):
    flavor = FlavorSerializer()

    class Meta:
        model = Tub
        fields = ["id", "flavor", "scoops_left"]
