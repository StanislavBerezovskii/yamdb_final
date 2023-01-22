"""
Файл с пермишнами для приложения api.
"""

from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    """Пермишн для админа и суперюзера."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin_or_superuser)


class IsAdminSuperUserOrReadOnly(permissions.BasePermission):
    """Пермишн для админа и суперюзера или только чтение."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin_or_superuser))


class IsStaffAuthorOrReadOnly(permissions.BasePermission):
    """Пермишн для админа, суперюзера, модератора, автора или только чтение."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (obj.author == request.user
                    or request.user.is_admin_or_superuser
                    or request.user.is_moderator))
