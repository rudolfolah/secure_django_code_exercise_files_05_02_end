from rest_framework import permissions

class OnlyCreatorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST' or request.method == 'GET'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.created_by

