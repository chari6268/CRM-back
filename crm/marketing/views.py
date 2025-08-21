from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    MarketingCampaign, EmailCampaign, EmailTemplate, EmailSubscriber,
    EmailSend, SocialMediaCampaign, MarketingAutomation, MarketingMetrics
)
from .serializers import (
    MarketingCampaignSerializer, EmailCampaignSerializer, EmailTemplateSerializer,
    EmailSubscriberSerializer, EmailSendSerializer, SocialMediaCampaignSerializer,
    MarketingAutomationSerializer, MarketingMetricsSerializer
)
from django.utils import timezone


class MarketingCampaignViewSet(viewsets.ModelViewSet):
    queryset = MarketingCampaign.objects.all()
    serializer_class = MarketingCampaignSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['campaign_type', 'status', 'created_by', 'assigned_to']
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'end_date', 'created_at']
    ordering = ['-start_date', '-created_at']

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        campaign = self.get_object()
        campaign.status = 'active'
        campaign.save()
        return Response({'status': 'Campaign activated'})

    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        campaign = self.get_object()
        campaign.status = 'paused'
        campaign.save()
        return Response({'status': 'Campaign paused'})


class EmailCampaignViewSet(viewsets.ModelViewSet):
    queryset = EmailCampaign.objects.all()
    serializer_class = EmailCampaignSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['email_type', 'campaign', 'created_by']
    search_fields = ['name', 'subject_line']
    ordering_fields = ['scheduled_at', 'sent_at', 'created_at']
    ordering = ['-scheduled_at', '-created_at']

    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        email_campaign = self.get_object()
        # Here you would implement the actual email sending logic
        email_campaign.sent_at = timezone.now()
        email_campaign.save()
        return Response({'status': 'Email campaign sent'})


class EmailTemplateViewSet(viewsets.ModelViewSet):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_active', 'created_by']
    search_fields = ['name', 'subject_line']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


class EmailSubscriberViewSet(viewsets.ModelViewSet):
    queryset = EmailSubscriber.objects.all()
    serializer_class = EmailSubscriberSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'source', 'company']
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['subscribed_at', 'created_at']
    ordering = ['-subscribed_at', '-created_at']

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        subscriber = self.get_object()
        subscriber.status = 'unsubscribed'
        subscriber.save()
        return Response({'status': 'Subscriber unsubscribed'})


class EmailSendViewSet(viewsets.ModelViewSet):
    queryset = EmailSend.objects.all()
    serializer_class = EmailSendSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'email_campaign', 'subscriber']
    search_fields = ['email_campaign__name', 'subscriber__email']
    ordering_fields = ['sent_at', 'opened_at', 'clicked_at']
    ordering = ['-sent_at']


class SocialMediaCampaignViewSet(viewsets.ModelViewSet):
    queryset = SocialMediaCampaign.objects.all()
    serializer_class = SocialMediaCampaignSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['platform', 'status', 'created_by']
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'end_date', 'created_at']
    ordering = ['-start_date', '-created_at']


class MarketingAutomationViewSet(viewsets.ModelViewSet):
    queryset = MarketingAutomation.objects.all()
    serializer_class = MarketingAutomationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['automation_type', 'status', 'created_by']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        automation = self.get_object()
        automation.status = 'active'
        automation.save()
        return Response({'status': 'Automation activated'})


class MarketingMetricsViewSet(viewsets.ModelViewSet):
    queryset = MarketingMetrics.objects.all()
    serializer_class = MarketingMetricsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['campaign', 'date', 'metric_type']
    search_fields = ['campaign__name']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date', '-created_at']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get marketing metrics summary"""
        total_impressions = sum(metric.impressions for metric in self.get_queryset())
        total_clicks = sum(metric.clicks for metric in self.get_queryset())
        total_conversions = sum(metric.conversions for metric in self.get_queryset())
        
        return Response({
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'total_conversions': total_conversions,
            'overall_ctr': (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        })
