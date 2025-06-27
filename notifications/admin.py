from django.contrib import admin
from .models import Announcement, AnnouncementView, AnnouncementComment, AnnouncementAttachment
admin.site.register(Announcement)
admin.site.register(AnnouncementView)
admin.site.register(AnnouncementComment)
admin.site.register(AnnouncementAttachment)