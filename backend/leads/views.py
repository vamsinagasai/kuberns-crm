from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Lead, Contact
from .serializers import (
    LeadSerializer, LeadCreateSerializer, LeadUpdateSerializer, ContactSerializer
)
from users.permissions import IsManagerOrAdmin, IsSalesExecutiveOrAbove


class LeadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Lead management.
    """
    queryset = Lead.objects.all()
    permission_classes = [IsAuthenticated, IsSalesExecutiveOrAbove]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Lead.objects.select_related('assigned_to', 'created_by').prefetch_related('contacts')
        
        # Sales executives see only their assigned leads
        if user.is_sales_executive():
            queryset = queryset.filter(assigned_to=user)
        
        # Filtering
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        city_filter = self.request.query_params.get('city')
        if city_filter:
            queryset = queryset.filter(city__icontains=city_filter)
        
        intent_filter = self.request.query_params.get('intent')
        if intent_filter:
            queryset = queryset.filter(intent=intent_filter)
        
        assigned_to_filter = self.request.query_params.get('assigned_to')
        if assigned_to_filter and (user.is_sales_manager() or user.is_admin_user()):
            queryset = queryset.filter(assigned_to_id=assigned_to_filter)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(company_name__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone__icontains=search) |
                Q(email__icontains=search)
            )
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return LeadCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return LeadUpdateSerializer
        return LeadSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        instance = serializer.instance
        new_status = serializer.validated_data.get('status', instance.status)
        
        # Validate won/lost reasons
        if new_status == 'won' and not serializer.validated_data.get('won_reason') and not instance.won_reason:
            raise serializers.ValidationError({
                'won_reason': 'Won reason is required when status is Won.'
            })
        if new_status == 'lost' and not serializer.validated_data.get('lost_reason') and not instance.lost_reason:
            raise serializers.ValidationError({
                'lost_reason': 'Lost reason is required when status is Lost.'
            })
        
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def at_risk(self, request):
        """Get leads without future tasks (at risk)."""
        from tasks.models import Task
        
        # Get all leads with no future tasks
        leads_with_tasks = Task.objects.filter(
            status='planned',
            scheduled_at__gte=timezone.now()
        ).values_list('lead_id', flat=True).distinct()
        
        queryset = self.get_queryset().exclude(id__in=leads_with_tasks)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get lead statistics for dashboard."""
        queryset = self.get_queryset()
        
        stats = {
            'total': queryset.count(),
            'by_status': dict(queryset.values('status').annotate(count=Count('id')).values_list('status', 'count')),
            'by_intent': dict(queryset.values('intent').annotate(count=Count('id')).values_list('intent', 'count')),
            'by_city': dict(queryset.values('city').annotate(count=Count('id')).values_list('city', 'count')),
        }
        
        return Response(stats)


class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Contact management.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsSalesExecutiveOrAbove]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Contact.objects.select_related('lead')
        
        if user.is_sales_executive():
            queryset = queryset.filter(lead__assigned_to=user)
        
        lead_id = self.request.query_params.get('lead')
        if lead_id:
            queryset = queryset.filter(lead_id=lead_id)
        
        return queryset
