from django.contrib import admin
from .models import Task, Visit


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['task_type', 'lead', 'scheduled_at', 'status', 'assigned_to', 'next_action_required']
    list_filter = ['task_type', 'status', 'scheduled_at']
    search_fields = ['lead__company_name', 'lead__first_name', 'lead__last_name']
    date_hierarchy = 'scheduled_at'


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['task', 'person_spoken_to', 'interest_level', 'meeting_permitted', 'created_at']
    list_filter = ['interest_level', 'meeting_permitted', 'meeting_declined', 'meeting_rescheduled']
    search_fields = ['task__lead__company_name', 'person_spoken_to']
