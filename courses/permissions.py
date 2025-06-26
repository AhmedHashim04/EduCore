from rest_framework import permissions
from .models import TermCourse

class IsCourseInstructor(permissions.BasePermission):
    def has_permission(self, request, view,course):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == 2 and 
                    TermCourse.objects.filter(instructor=request.user, course=course).exists())


class IsCourseStudent(permissions.BasePermission):

        def has_permission(self, request, view,course):
            return bool(request.user and request.user.is_authenticated and request.user.user_type == 3 and 
                        TermCourse.objects.filter(instructor=request.user, course=course).exists())

class IsCourseStaff(permissions.BasePermission):
    pass
    