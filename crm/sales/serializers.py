from rest_framework import serializers
from .models import Lead, Opportunity, Deal, SalesActivity, SalesPipeline, SalesForecast
from crm.core.serializers import CustomerSerializer, UserSerializer


class LeadSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Lead
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class OpportunitySerializer(serializers.ModelSerializer):
    lead = LeadSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Opportunity
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class DealSerializer(serializers.ModelSerializer):
    opportunity = OpportunitySerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Deal
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class SalesActivitySerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    related_lead = LeadSerializer(read_only=True)
    related_opportunity = OpportunitySerializer(read_only=True)
    
    class Meta:
        model = SalesActivity
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class SalesPipelineSerializer(serializers.ModelSerializer):
    stages = serializers.JSONField()
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = SalesPipeline
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class SalesForecastSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = SalesForecast
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
