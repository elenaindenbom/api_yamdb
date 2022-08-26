from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view,):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_admin or request.user.is_superuser))  # добавить методы is_admin, is_moderator в User
