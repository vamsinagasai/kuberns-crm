from rest_framework import serializers
from .models import Task, Visit
from leads.serializers import LeadSerializer
from users.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model."""
    lead_detail = LeadSerializer(source='lead', read_only=True)
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'task_type', 'lead', 'lead_detail', 'scheduled_at',
            'assigned_to', 'assigned_to_detail', 'status', 'outcome_notes',
            'next_action_required', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class VisitSerializer(serializers.ModelSerializer):
    """Serializer for Visit model."""
    task_detail = TaskSerializer(source='task', read_only=True)
    
    class Meta:
        model = Visit
        fields = [
            'id', 'task', 'task_detail',
            'person_spoken_to', 'person_role', 'frameworks_discussed',
            'confirmed_client_types', 'infrastructure_discussed',
            'deployment_pain_points', 'time_spent_on_deployments',
            'cost_spent_on_deployments', 'effort_and_team_involved',
            'partnership_interest', 'interest_level', 'cloud_spending_range',
            'demo_video_shared', 'kuberns_explained_clearly', 'roadmap_clear',
            'deployment_roadmap', 'next_steps_agreed',
            'meeting_permitted', 'meeting_declined', 'decline_reason',
            'meeting_rescheduled', 'reschedule_reason', 'suggested_followup_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tasks."""
    
    class Meta:
        model = Task
        fields = [
            'task_type', 'lead', 'scheduled_at', 'assigned_to',
            'status', 'outcome_notes', 'next_action_required'
        ]
    
    def create(self, validated_data):
        # Default assigned_to to current user if not provided
        if 'assigned_to' not in validated_data:
            validated_data['assigned_to'] = self.context['request'].user
        return super().create(validated_data)


class VisitCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating visit with task."""
    task_data = TaskCreateSerializer(write_only=True)
    
    class Meta:
        model = Visit
        fields = [
            'task_data',
            'person_spoken_to', 'person_role', 'frameworks_discussed',
            'confirmed_client_types', 'infrastructure_discussed',
            'deployment_pain_points', 'time_spent_on_deployments',
            'cost_spent_on_deployments', 'effort_and_team_involved',
            'partnership_interest', 'interest_level', 'cloud_spending_range',
            'demo_video_shared', 'kuberns_explained_clearly', 'roadmap_clear',
            'deployment_roadmap', 'next_steps_agreed',
            'meeting_permitted', 'meeting_declined', 'decline_reason',
            'meeting_rescheduled', 'reschedule_reason', 'suggested_followup_date',
        ]
    
    def create(self, validated_data):
        task_data = validated_data.pop('task_data')
        task_data['task_type'] = 'visit'
        task_serializer = TaskCreateSerializer(data=task_data, context=self.context)
        task_serializer.is_valid(raise_exception=True)
        task = task_serializer.save()
        
        visit = Visit.objects.create(task=task, **validated_data)
        return visit
