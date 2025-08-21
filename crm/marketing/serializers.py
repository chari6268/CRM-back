from rest_framework import serializers
from .models import (
    MarketingCampaign, EmailCampaign, EmailTemplate, EmailSubscriber,
    EmailSend, SocialMediaCampaign, MarketingAutomation, MarketingMetrics
)
from crm.core.serializers import UserSerializer, CompanySerializer


class MarketingCampaignSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    
    class Meta:
        model = MarketingCampaign
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmailCampaignSerializer(serializers.ModelSerializer):
    campaign = MarketingCampaignSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = EmailCampaign
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmailTemplateSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = EmailTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmailSubscriberSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    
    class Meta:
        model = EmailSubscriber
        fields = '__all__'
        read_only_fields = ['id', 'subscribed_at', 'created_at']


class EmailSendSerializer(serializers.ModelSerializer):
    email_campaign = EmailCampaignSerializer(read_only=True)
    subscriber = EmailSubscriberSerializer(read_only=True)
    
    class Meta:
        model = EmailSend
        fields = '__all__'
        read_only_fields = ['id', 'sent_at', 'opened_at', 'clicked_at']


class SocialMediaCampaignSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = SocialMediaCampaign
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class MarketingAutomationSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = MarketingAutomation
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class MarketingMetricsSerializer(serializers.ModelSerializer):
    campaign = MarketingCampaignSerializer(read_only=True)
    
    class Meta:
        model = MarketingMetrics
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
