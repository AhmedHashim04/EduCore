from rest_framework import permissions

class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 1

class ProfessorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 2

class StudentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 3

class StaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 4
