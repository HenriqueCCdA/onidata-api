from rest_framework.permissions import BasePermission


class OnlyUserCanAccessOwnLoan(BasePermission):
    """Shelter only can delete and update own pets"""

    def has_object_permission(self, request, view, obj):
        return obj.user.pk == request.user.pk
