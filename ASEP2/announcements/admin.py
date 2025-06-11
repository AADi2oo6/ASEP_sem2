from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    # list_display = ('subject', 'teacher_name', 'teacher_id', 'created_at')
    list_display = (
        "teacher_id",
        "teacher_name",
        "subject",
        "content",
        "attachment",
        "years",
        "branches",
        "sections",
        "batches",
        "created_at",)
    search_fields = ('teacher_name', 'teacher_id', 'subject')
    list_filter = ('created_at', 'branches', 'sections', 'years')
