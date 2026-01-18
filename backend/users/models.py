from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with role-based access control.
    """
    ROLE_CHOICES = [
        ('sales_executive', 'Sales Executive'),
        ('sales_manager', 'Sales Manager'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='sales_executive')
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100, blank=True, help_text="Assigned city/territory")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    def is_sales_executive(self):
        return self.role == 'sales_executive'
    
    def is_sales_manager(self):
        return self.role == 'sales_manager'
    
    def is_admin_user(self):
        return self.role == 'admin'
