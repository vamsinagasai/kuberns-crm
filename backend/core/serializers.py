from rest_framework import serializers
from .models import AuditLog, ActivityLog
from users.serializers import UserSerializer


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer for AuditLog model."""
    user_detail = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_detail', 'action', 'content_type',
            'object_id', 'changes', 'ip_address', 'user_agent', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for ActivityLog model."""
    user_detail = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = ActivityLog
        fields = [
            'id', 'user', 'user_detail', 'date', 'visits_count',
            'calls_count', 'meetings_count', 'followups_scheduled',
            'leads_updated', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
