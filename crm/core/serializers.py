from rest_framework import serializers
from .models import User, Company, Customer, Interaction, Task, Notification


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'avatar', 'department', 'position', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for Company model."""
    customer_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'industry', 'size', 'website', 'address',
            'phone', 'email', 'logo', 'is_active', 'customer_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_customer_count(self, obj):
        return obj.customers.count()


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model."""
    company_name = serializers.CharField(source='company.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Customer
        fields = [
            'id', 'company', 'company_name', 'first_name', 'last_name',
            'full_name', 'email', 'phone', 'position', 'status', 'source',
            'assigned_to', 'assigned_to_name', 'notes', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.full_name


class InteractionSerializer(serializers.ModelSerializer):
    """Serializer for Interaction model."""
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Interaction
        fields = [
            'id', 'customer', 'customer_name', 'user', 'user_name', 'type',
            'subject', 'description', 'date', 'duration', 'outcome',
            'next_action', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model."""
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'assigned_to', 'assigned_to_name',
            'customer', 'customer_name', 'priority', 'status', 'due_date',
            'completed_at', 'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model."""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'user_name', 'type', 'title', 'message',
            'is_read', 'related_url', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics."""
    total_customers = serializers.IntegerField()
    total_companies = serializers.IntegerField()
    active_tasks = serializers.IntegerField()
    pending_interactions = serializers.IntegerField()
    recent_activities = serializers.ListField()
    upcoming_deadlines = serializers.ListField()
