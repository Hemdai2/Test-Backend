from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from glace.models import Tub
from glace.serializers import TubSerializer


@api_view(["POST"])
@permission_classes([IsAdminUser])
def refill_tub(request, tub_id):
    """
    Remplir un pot de glace, accès seulement aux admins
    """
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
