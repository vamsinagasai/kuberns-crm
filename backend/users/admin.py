from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'city', 'is_active']
    list_filter = ['role', 'is_active', 'city']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Kuberns CRM Info', {'fields': ('role', 'phone', 'city')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Kuberns CRM Info', {'fields': ('role', 'phone', 'city', 'email', 'first_name', 'last_name')}),
    )
