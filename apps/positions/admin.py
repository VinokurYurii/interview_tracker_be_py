from django.contrib import admin

from apps.positions.models import Position

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "status", "user")
