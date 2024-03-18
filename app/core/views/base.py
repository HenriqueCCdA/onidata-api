from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from app.core.services import extract_client_id


@extend_schema(tags=["debug"])
@api_view(["GET"])
@permission_classes([])
def get_client_ip(request):
    """Retorna o IP do client"""
    return Response({"client_ip": extract_client_id(request.META)})


@extend_schema(tags=["root"])
@api_view(["GET"])
@permission_classes([])
def root(request):
    """Pagina root"""
    return Response(
        {
            "api": "anidata-api",
            "doc_ref": "/docs/",
        }
    )
