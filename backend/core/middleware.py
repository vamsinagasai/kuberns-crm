import json
from django.utils import timezone
from .models import AuditLog


class AuditLogMiddleware:
    """
    Middleware to log all changes to Lead and Task models.
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Track changes in API views.
        """
        if not request.user.is_authenticated:
            return None
        
        # Store request info for later use in process_response
        request._audit_info = {
            'user': request.user,
            'ip_address': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', '')[:255],
        }
        return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


def log_audit(user, action, instance, changes=None, ip_address=None, user_agent=None):
    """
    Helper function to create audit log entries.
    """
    from django.contrib.contenttypes.models import ContentType
    
    content_type = ContentType.objects.get_for_model(instance)
    AuditLog.objects.create(
        user=user,
        action=action,
        content_type=content_type,
        object_id=instance.pk,
        changes=changes or {},
        ip_address=ip_address,
        user_agent=user_agent or ''
    )
