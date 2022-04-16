from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == "admin"


class IsAuthorOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role in ["admin", "moderator"]
            or obj.author == request.user
        )
