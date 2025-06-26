from django.contrib import admin
from .models import Enrollment, StudentProfile, Attendance

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'grade', 'is_active')
    search_fields = ('student__username', 'course__course__title')
    list_filter = ('course', 'grade', 'is_active', 'withdrawn')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student', 'program', 'enrollment_date', 'gpa')
    search_fields = ('student__username', 'program__name')
    list_filter = ('program',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status')
    search_fields = ('student__username', 'termcourse__course__title')
    list_filter = ('course', 'status', 'date')