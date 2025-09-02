from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return getattr(user, 'role', None) in ('admin', 'manager') or user.is_superuser


class IsOwnerOrAdminReadOnly(BasePermission):
    """Allow owners to edit their facility; others read-only unless admin/manager."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, 'role', None) in ('admin', 'manager') or user.is_superuser:
            return True
        return getattr(obj, 'owner_id', None) == user.id
