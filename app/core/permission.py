# from rest_framework.permissions import BasePermission


# class OnlyUserCanAccessOwnLoan(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.loan.user.pk == request.user.pk
