from rest_framework import serializers
from .models import (
    SupportTicket, TicketResponse, ServiceLevelAgreement, KnowledgeBase,
    CustomerFeedback, SupportTeam, SupportMetrics
)
from crm.core.serializers import UserSerializer, CustomerSerializer


class SupportTicketSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    
    class Meta:
        model = SupportTicket
        fields = '__all__'
        read_only_fields = ['id', 'ticket_number', 'created_at', 'updated_at', 'resolved_at', 'closed_at']


class TicketResponseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    ticket = SupportTicketSerializer(read_only=True)
    
    class Meta:
        model = TicketResponse
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class ServiceLevelAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceLevelAgreement
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = KnowledgeBase
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'view_count']


class CustomerFeedbackSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    
    class Meta:
        model = CustomerFeedback
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class SupportTeamSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = SupportTeam
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class SupportMetricsSerializer(serializers.ModelSerializer):
    team = SupportTeamSerializer(read_only=True)
    
    class Meta:
        model = SupportMetrics
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
