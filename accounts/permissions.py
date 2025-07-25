# permissions.py
from rest_framework.permissions import BasePermission
from .models import UserType

class IsAdminUserType(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == UserType.ADMIN
class IsAdminUserOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.user_type == UserType.ADMIN
        )