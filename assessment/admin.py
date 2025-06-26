from django.contrib import admin
from .models import Assignment, Submission, Exam, Grade

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_offering', 'due_date', 'total_points')
    search_fields = ('title', 'course_offering__course__title')
    list_filter = ('course_offering',)

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'grade')
    search_fields = ('assignment__title', 'student__username')
    list_filter = ('assignment', 'is_late')

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_offering', 'exam_type', 'date', 'total_points')
    search_fields = ('title', 'course_offering__course__title')
    list_filter = ('exam_type', 'course_offering')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'score', 'published')
    search_fields = ('exam__title', 'student__username')
    list_filter = ('exam', 'published')