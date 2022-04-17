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


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            # request.method in permissions.SAFE_METHODS
            request.user.is_authenticated
            and request.user.role == "admin"
        ):
            return True

    def has_object_permission(self, request, view, obj):
        return True


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.is_authenticated
            and request.user.role == "admin"
            or request.user.is_staff 
            and request.user.is_authenticated
        ):
            return True

    def has_object_permission(self, request, view, obj):
        return True
