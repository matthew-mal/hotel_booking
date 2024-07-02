from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (obj.user == request.user or request.user.is_staff)
        )


class AdminOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        # Разрешаем GET запросы всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверяем, является ли пользователь администратором
        return request.user and request.user.is_superuser
