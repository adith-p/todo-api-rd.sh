from rest_framework.permissions import BasePermission
from .models import Todo


class CustomIsAuthPermission(BasePermission):
    message = {"message": "Unauthorized"}

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class CustomIsAuthorPermission(BasePermission):
    message = {"message": "Forbidden"}

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user
