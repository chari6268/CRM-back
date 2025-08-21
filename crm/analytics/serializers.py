from rest_framework import serializers
from .models import (
    ChurnRisk, CustomerMetrics, SentimentAnalysis, ProductFeedback
)
from crm.core.serializers import CustomerSerializer


class ChurnRiskSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    
    class Meta:
        model = ChurnRisk
        fields = '__all__'
        read_only_fields = ['id', 'last_calculated', 'created_at']


class CustomerMetricsSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    
    class Meta:
        model = CustomerMetrics
        fields = '__all__'
        read_only_fields = ['id', 'date', 'created_at']


class SentimentAnalysisSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    
    class Meta:
        model = SentimentAnalysis
        fields = '__all__'
        read_only_fields = ['id', 'date', 'created_at']


class ProductFeedbackSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    
    class Meta:
        model = ProductFeedback
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
