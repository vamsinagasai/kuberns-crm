from django.contrib import admin
from .models import Lead, Contact


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'first_name', 'last_name', 'status', 'city', 
                    'intent', 'assigned_to', 'created_at']
    list_filter = ['status', 'intent', 'city', 'infrastructure', 'client_type']
    search_fields = ['company_name', 'first_name', 'last_name', 'phone', 'email']
    inlines = [ContactInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'lead', 'decision_maker', 'phone']
    list_filter = ['decision_maker']
    search_fields = ['name', 'lead__company_name']
