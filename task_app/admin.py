from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'status', 'priority', 'assignee')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'board__title')
