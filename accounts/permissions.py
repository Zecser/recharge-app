# permissions.py
from rest_framework.permissions import BasePermission
from .models import UserType

class IsAdminUserOnly(BasePermission):
    """
    Allows access only to users with user_type='Admin'.
    """

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.user_type == UserType.ADMIN
        )
    
