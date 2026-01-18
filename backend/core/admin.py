from django.contrib import admin
from .models import AuditLog, ActivityLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'content_type', 'object_id', 'created_at']
    list_filter = ['action', 'content_type', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['user', 'action', 'content_type', 'object_id', 'changes', 
                      'ip_address', 'user_agent', 'created_at']
    date_hierarchy = 'created_at'


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'visits_count', 'calls_count', 'meetings_count', 'followups_scheduled']
    list_filter = ['date']
    search_fields = ['user__username']
    date_hierarchy = 'date'
