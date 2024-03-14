from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from app import __version__


@extend_schema(tags=["core"])
@api_view(["GET"])
@permission_classes([])
def api_version(request):
    """Mostra a versão da api"""
    return Response({"version": __version__})
