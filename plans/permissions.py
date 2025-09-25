from rest_framework import permissions

class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Only users with specific roles can create or edit plans.
    Others (e.g. players) can only view (read-only).
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # TODO: to write right profiles
        # Allow create/edit only for specific roles
        return (
            request.user.is_superuser or
            getattr(request.user, 'role', None) in [
            'coach', 'dietitian', 'physiotherapist', 'manager'
        ] )