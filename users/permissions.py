from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 1

class IsProfessor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 2

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 3

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 4
