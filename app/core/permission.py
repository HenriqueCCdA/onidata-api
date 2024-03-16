from rest_framework.permissions import BasePermission


class UserOnlyCanAccessOwnLoan(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.pk == request.user.pk


class UserOnlyCanAccessOwnPayment(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.loan.user.pk == request.user.pk
