from django.db import models
from django.conf import settings


class Task(models.Model):
    """
    Task model for tracking visits, calls, meetings, and WhatsApp follow-ups.
    """
    TASK_TYPE_CHOICES = [
        ('visit', 'Visit'),
        ('online_meeting', 'Online Meeting'),
        ('call', 'Call'),
        ('whatsapp', 'WhatsApp'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
    ]
    
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    lead = models.ForeignKey('leads.Lead', on_delete=models.CASCADE, related_name='tasks')
    scheduled_at = models.DateTimeField()
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='tasks'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    outcome_notes = models.TextField(blank=True)
    next_action_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tasks'
        ordering = ['scheduled_at']
        indexes = [
            models.Index(fields=['status', 'scheduled_at']),
            models.Index(fields=['lead', 'status']),
            models.Index(fields=['assigned_to', 'scheduled_at']),
        ]
    
    def __str__(self):
        return f"{self.get_task_type_display()} - {self.lead.company_name} - {self.scheduled_at}"


class Visit(models.Model):
    """
    Detailed visit information for on-field visits.
    """
    INTEREST_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='visit_details')
    
    # Meeting Details
    person_spoken_to = models.CharField(max_length=100, blank=True)
    person_role = models.CharField(max_length=100, blank=True)
    frameworks_discussed = models.JSONField(default=list, blank=True)
    confirmed_client_types = models.CharField(max_length=20, blank=True)
    infrastructure_discussed = models.CharField(max_length=20, blank=True)
    
    # Pain Discovery
    deployment_pain_points = models.TextField(blank=True)
    time_spent_on_deployments = models.CharField(max_length=50, blank=True)
    cost_spent_on_deployments = models.CharField(max_length=50, blank=True)
    effort_and_team_involved = models.TextField(blank=True)
    
    # Kuberns Fit
    partnership_interest = models.CharField(
        max_length=20,
        choices=[('yes', 'Yes'), ('no', 'No'), ('not_discussed', 'Not discussed')],
        default='not_discussed'
    )
    interest_level = models.CharField(max_length=10, choices=INTEREST_LEVEL_CHOICES, blank=True)
    cloud_spending_range = models.CharField(max_length=50, blank=True)
    demo_video_shared = models.BooleanField(default=False)
    kuberns_explained_clearly = models.BooleanField(default=False)
    roadmap_clear = models.BooleanField(default=False)
    
    # Roadmap
    deployment_roadmap = models.TextField(blank=True)
    next_steps_agreed = models.TextField(blank=True)
    
    # Meeting Status
    meeting_permitted = models.BooleanField(default=True)
    meeting_declined = models.BooleanField(default=False)
    decline_reason = models.TextField(blank=True)
    meeting_rescheduled = models.BooleanField(default=False)
    reschedule_reason = models.TextField(blank=True)
    suggested_followup_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'visits'
    
    def __str__(self):
        return f"Visit - {self.task.lead.company_name} - {self.task.scheduled_at}"
