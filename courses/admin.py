from django.contrib import admin
from .models import Course, TermCourse

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'department', 'is_core', 'is_active')
    search_fields = ('code', 'title')
    list_filter = ('department', 'is_core', 'is_active')

@admin.register(TermCourse)
class TermCourseAdmin(admin.ModelAdmin):
    list_display = ('course', 'semester', 'instructor', 'is_active')
    search_fields = ('course__code', 'course__title')
    list_filter = ('semester', 'instructor', 'is_active')