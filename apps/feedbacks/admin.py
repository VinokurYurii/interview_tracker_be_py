from django.contrib import admin

from apps.feedbacks.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("feedback_type", "interview_stage", "content")
