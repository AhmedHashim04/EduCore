from django.contrib import admin
from .models import Announcement, Resource

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'target_audience', 'is_important')
    search_fields = ('title', 'content')
    list_filter = ('target_audience', 'is_important', 'created_at')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'uploaded_by', 'uploaded_at', 'is_public')
    search_fields = ('title', 'description')
    list_filter = ('resource_type', 'is_public', 'course_offering')