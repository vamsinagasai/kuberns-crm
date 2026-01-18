from rest_framework import permissions


class IsManagerOrAdmin(permissions.BasePermission):
    """Permission for Sales Manager or Admin only."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_sales_manager() or request.user.is_admin_user()
        )


class IsAdminOrSelf(permissions.BasePermission):
    """Permission for Admin or the user themselves."""
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin_user() or obj == request.user


class IsSalesExecutiveOrAbove(permissions.BasePermission):
    """Permission for Sales Executive or above."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
