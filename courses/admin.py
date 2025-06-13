from django.contrib import admin
from .models import Course, CourseOffering

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'department', 'credits', 'is_core', 'is_active')
    search_fields = ('code', 'title')
    list_filter = ('department', 'is_core', 'is_active')

@admin.register(CourseOffering)
class CourseOfferingAdmin(admin.ModelAdmin):
    list_display = ('course', 'semester', 'section', 'instructor', 'is_active')
    search_fields = ('course__code', 'course__title')
    list_filter = ('semester', 'instructor', 'is_active')