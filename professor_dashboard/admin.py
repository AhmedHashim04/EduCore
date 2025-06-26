from django.contrib import admin
from .models import ProfessorProfile

@admin.register(ProfessorProfile)
class ProfessorProfileAdmin(admin.ModelAdmin):
    list_display = ('professor', 'department', 'position')
    search_fields = ('professor__username', 'department__name')
    list_filter = ('department', 'position')