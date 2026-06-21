from django.contrib import admin

from apps.interview_stages.models import InterviewStage

@admin.register(InterviewStage)
class InterviewStageAdmin(admin.ModelAdmin):
    list_display = ("stage_type", "status", "position", "scheduled_at")
