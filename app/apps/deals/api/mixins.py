from rest_framework import permissions


class IsBoss(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.exclude(name='Риелтор'):
            return True
        return False