from django.contrib import admin
from .models import Department, Program, Semester

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head_of_department')
    search_fields = ('name', 'code')
    list_filter = ('established_date',)

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'degree')
    search_fields = ('name', 'code')
    list_filter = ('department', 'degree')

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('year', 'semester', 'start_date', 'end_date', 'is_current')
    list_filter = ('semester', 'is_current')
    ordering = ('-year', 'semester')