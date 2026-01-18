from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta, date
from .models import AuditLog, ActivityLog
from .serializers import AuditLogSerializer, ActivityLogSerializer
from users.permissions import IsManagerOrAdmin, IsSalesExecutiveOrAbove


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing audit logs.
    """
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    
    def get_queryset(self):
        queryset = AuditLog.objects.select_related('user', 'content_type')
        
        # Filter by content type
        content_type = self.request.query_params.get('content_type')
        if content_type:
            queryset = queryset.filter(content_type__model=content_type)
        
        # Filter by object_id
        object_id = self.request.query_params.get('object_id')
        if object_id:
            queryset = queryset.filter(object_id=object_id)
        
        # Filter by user
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset


class ActivityLogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for activity logs.
    """
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated, IsSalesExecutiveOrAbove]
    
    def get_queryset(self):
        user = self.request.user
        queryset = ActivityLog.objects.select_related('user')
        
        # Sales executives see only their activity
        if user.is_sales_executive():
            queryset = queryset.filter(user=user)
        
        # Filter by date range
        date_from = self.request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        
        date_to = self.request.query_params.get('date_to')
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get or create today's activity log."""
        today = date.today()
        activity_log, created = ActivityLog.objects.get_or_create(
            user=request.user,
            date=today,
            defaults={
                'visits_count': 0,
                'calls_count': 0,
                'meetings_count': 0,
                'followups_scheduled': 0,
                'leads_updated': 0,
            }
        )
        serializer = self.get_serializer(activity_log)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get activity statistics."""
        user = request.user
        queryset = ActivityLog.objects.filter(user=user)
        
        # Only managers/admins can see all users' stats
        if not user.is_sales_executive():
            user_id = request.query_params.get('user_id')
            if user_id:
                queryset = ActivityLog.objects.filter(user_id=user_id)
        
        # Date range
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        stats = queryset.aggregate(
            total_visits=Count('visits_count'),
            total_calls=Count('calls_count'),
            total_meetings=Count('meetings_count'),
            total_followups=Count('followups_scheduled'),
            total_leads_updated=Count('leads_updated'),
        )
        
        return Response(stats)
