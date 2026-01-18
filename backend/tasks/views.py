from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Task, Visit
from .serializers import (
    TaskSerializer, TaskCreateSerializer, VisitSerializer, VisitCreateSerializer
)
from users.permissions import IsSalesExecutiveOrAbove, IsManagerOrAdmin


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Task management.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsSalesExecutiveOrAbove]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.select_related('lead', 'assigned_to')
        
        # Sales executives see only their tasks
        if user.is_sales_executive():
            queryset = queryset.filter(assigned_to=user)
        
        # Filtering
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        task_type_filter = self.request.query_params.get('task_type')
        if task_type_filter:
            queryset = queryset.filter(task_type=task_type_filter)
        
        lead_id = self.request.query_params.get('lead')
        if lead_id:
            queryset = queryset.filter(lead_id=lead_id)
        
        # Date filters
        date_from = self.request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(scheduled_at__gte=date_from)
        
        date_to = self.request.query_params.get('date_to')
        if date_to:
            queryset = queryset.filter(scheduled_at__lte=date_to)
        
        # Today's tasks
        today = self.request.query_params.get('today')
        if today == 'true':
            today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            queryset = queryset.filter(scheduled_at__gte=today_start, scheduled_at__lt=today_end)
        
        # Overdue tasks
        overdue = self.request.query_params.get('overdue')
        if overdue == 'true':
            queryset = queryset.filter(
                status='planned',
                scheduled_at__lt=timezone.now()
            )
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        return TaskSerializer
    
    def perform_create(self, serializer):
        # Default to current user if assigned_to not provided
        if 'assigned_to' not in serializer.validated_data:
            serializer.save(assigned_to=self.request.user)
        else:
            serializer.save()
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark task as completed and optionally create next action."""
        task = self.get_object()
        outcome_notes = request.data.get('outcome_notes', '')
        next_action_required = request.data.get('next_action_required', False)
        next_action_data = request.data.get('next_action', None)
        
        task.status = 'completed'
        task.outcome_notes = outcome_notes
        task.next_action_required = next_action_required
        task.save()
        
        # Create next action if required
        if next_action_required and next_action_data:
            next_task = Task.objects.create(
                task_type=next_action_data.get('task_type', 'call'),
                lead=task.lead,
                scheduled_at=next_action_data.get('scheduled_at'),
                assigned_to=task.assigned_to,
                status='planned'
            )
            serializer = self.get_serializer(next_task)
            return Response({
                'task': self.get_serializer(task).data,
                'next_action': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(self.get_serializer(task).data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def calendar(self, request):
        """Get tasks in calendar format."""
        queryset = self.get_queryset()
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        if date_from and date_to:
            queryset = queryset.filter(scheduled_at__gte=date_from, scheduled_at__lte=date_to)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class VisitViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Visit management.
    """
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated, IsSalesExecutiveOrAbove]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Visit.objects.select_related('task', 'task__lead', 'task__assigned_to')
        
        if user.is_sales_executive():
            queryset = queryset.filter(task__assigned_to=user)
        
        lead_id = self.request.query_params.get('lead')
        if lead_id:
            queryset = queryset.filter(task__lead_id=lead_id)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return VisitCreateSerializer
        return VisitSerializer
