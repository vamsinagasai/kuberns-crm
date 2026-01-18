from rest_framework import serializers
from .models import Lead, Contact
from users.serializers import UserSerializer


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact model."""
    
    class Meta:
        model = Contact
        fields = ['id', 'name', 'role', 'phone', 'email', 'decision_maker', 'created_at']
        read_only_fields = ['id', 'created_at']


class LeadSerializer(serializers.ModelSerializer):
    """Serializer for Lead model."""
    contacts = ContactSerializer(many=True, read_only=True)
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)
    created_by_detail = UserSerializer(source='created_by', read_only=True)
    
    class Meta:
        model = Lead
        fields = [
            'id', 'status', 'first_name', 'last_name', 'company_name', 'company_size',
            'industry', 'city', 'state', 'phone', 'email',
            'frameworks_used', 'infrastructure', 'client_type', 'cloud_spending',
            'decision_maker', 'role',
            'intent', 'research_notes', 'closing_strategy', 'partnership_interest',
            'won_reason', 'lost_reason',
            'assigned_to', 'assigned_to_detail', 'created_by', 'created_by_detail',
            'contacts', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    def validate_status(self, value):
        """Ensure won/lost reasons are provided when status changes."""
        if value in ['won', 'lost']:
            # This will be checked in the view
            pass
        return value


class LeadCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating leads."""
    contacts = ContactSerializer(many=True, required=False)
    
    class Meta:
        model = Lead
        fields = [
            'status', 'first_name', 'last_name', 'company_name', 'company_size',
            'industry', 'city', 'state', 'phone', 'email',
            'frameworks_used', 'infrastructure', 'client_type', 'cloud_spending',
            'decision_maker', 'role',
            'intent', 'research_notes', 'closing_strategy', 'partnership_interest',
            'assigned_to', 'contacts'
        ]
    
    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts', [])
        lead = Lead.objects.create(
            created_by=self.context['request'].user,
            **validated_data
        )
        for contact_data in contacts_data:
            Contact.objects.create(lead=lead, **contact_data)
        return lead


class LeadUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating leads."""
    contacts = ContactSerializer(many=True, required=False)
    
    class Meta:
        model = Lead
        fields = [
            'status', 'first_name', 'last_name', 'company_name', 'company_size',
            'industry', 'city', 'state', 'phone', 'email',
            'frameworks_used', 'infrastructure', 'client_type', 'cloud_spending',
            'decision_maker', 'role',
            'intent', 'research_notes', 'closing_strategy', 'partnership_interest',
            'won_reason', 'lost_reason',
            'assigned_to', 'contacts'
        ]
    
    def update(self, instance, validated_data):
        contacts_data = validated_data.pop('contacts', None)
        
        # Update lead fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update contacts if provided
        if contacts_data is not None:
            # Delete existing contacts and create new ones
            instance.contacts.all().delete()
            for contact_data in contacts_data:
                Contact.objects.create(lead=instance, **contact_data)
        
        return instance
