from django.db import models
from django.conf import settings


class Lead(models.Model):
    """
    Core Lead model for tracking IT agencies and partnerships.
    """
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('sales_nurture', 'Sales Nurture'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]
    
    INTENT_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    INFRASTRUCTURE_CHOICES = [
        ('aws', 'AWS'),
        ('azure', 'Azure'),
        ('gcp', 'GCP'),
        ('on_prem', 'On-prem'),
        ('mixed', 'Mixed'),
    ]
    
    CLIENT_TYPE_CHOICES = [
        ('indian', 'Indian'),
        ('foreign', 'Foreign'),
        ('both', 'Both'),
    ]
    
    # Basic Information
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200)
    company_size = models.CharField(max_length=50, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    
    # Business & Technical Context
    frameworks_used = models.JSONField(default=list, blank=True, help_text="List of frameworks")
    infrastructure = models.CharField(max_length=20, choices=INFRASTRUCTURE_CHOICES, blank=True)
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES, blank=True)
    cloud_spending = models.CharField(max_length=50, blank=True, help_text="Monthly estimate")
    decision_maker = models.BooleanField(default=False)
    role = models.CharField(max_length=100, blank=True)
    
    # Sales Intelligence
    intent = models.CharField(max_length=10, choices=INTENT_CHOICES, blank=True)
    research_notes = models.TextField(blank=True)
    closing_strategy = models.TextField(blank=True)
    partnership_interest = models.CharField(
        max_length=20,
        choices=[('yes', 'Yes'), ('no', 'No'), ('not_discussed', 'Not discussed')],
        default='not_discussed'
    )
    
    # Outcome
    won_reason = models.TextField(blank=True)
    lost_reason = models.TextField(blank=True)
    
    # Assignment & Tracking
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_leads'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_leads'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leads'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['status', 'assigned_to']),
            models.Index(fields=['city']),
            models.Index(fields=['intent']),
        ]
    
    def __str__(self):
        return f"{self.company_name} - {self.first_name} {self.last_name}"


class Contact(models.Model):
    """
    Additional contact persons for a lead.
    """
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    decision_maker = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'contacts'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.lead.company_name})"
