from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Проверка на наличие прав модератора."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moderators').exists()


class IsOwner(BasePermission):
    """Проверка, является ли пользователь владельцем или суперпользователем."""
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False

