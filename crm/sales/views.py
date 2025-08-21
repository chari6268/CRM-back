from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Lead, Opportunity, Deal, SalesActivity, SalesPipeline, SalesForecast
from .serializers import (
    LeadSerializer, OpportunitySerializer, DealSerializer,
    SalesActivitySerializer, SalesPipelineSerializer, SalesForecastSerializer
)


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'lead_source', 'assigned_to', 'company_name']
    search_fields = ['first_name', 'last_name', 'company_name', 'email']
    ordering_fields = ['lead_score', 'created_at', 'last_contacted']
    ordering = ['-lead_score', '-created_at']

    @action(detail=True, methods=['post'])
    def qualify(self, request, pk=None):
        lead = self.get_object()
        lead.status = 'qualified'
        lead.save()
        return Response({'status': 'Lead qualified'})

    @action(detail=True, methods=['post'])
    def convert(self, request, pk=None):
        lead = self.get_object()
        lead.status = 'converted'
        lead.save()
        return Response({'status': 'Lead converted'})


class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['stage', 'assigned_to', 'customer', 'probability']
    search_fields = ['title', 'description']
    ordering_fields = ['amount', 'expected_close_date', 'probability']
    ordering = ['-expected_close_date', '-amount']

    @action(detail=True, methods=['post'])
    def advance_stage(self, request, pk=None):
        opportunity = self.get_object()
        current_stage = opportunity.stage
        stages = ['prospecting', 'qualification', 'needs_analysis', 'proposal', 'negotiation', 'closed_won']
        
        try:
            current_index = stages.index(current_stage)
            if current_index < len(stages) - 1:
                opportunity.stage = stages[current_index + 1]
                opportunity.save()
                return Response({'status': f'Advanced to {opportunity.stage}'})
            else:
                return Response({'error': 'Already at final stage'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Invalid stage'}, status=status.HTTP_400_BAD_REQUEST)


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'assigned_to', 'customer', 'deal_type']
    search_fields = ['title', 'description']
    ordering_fields = ['amount', 'close_date', 'created_at']
    ordering = ['-close_date', '-amount']

    @action(detail=True, methods=['post'])
    def close_deal(self, request, pk=None):
        deal = self.get_object()
        deal.status = 'closed'
        deal.save()
        return Response({'status': 'Deal closed'})


class SalesActivityViewSet(viewsets.ModelViewSet):
    queryset = SalesActivity.objects.all()
    serializer_class = SalesActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['activity_type', 'assigned_to', 'related_lead', 'related_opportunity']
    search_fields = ['subject', 'description']
    ordering_fields = ['due_date', 'created_at', 'completed_at']
    ordering = ['-due_date', '-created_at']

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        activity = self.get_object()
        activity.status = 'completed'
        activity.save()
        return Response({'status': 'Activity completed'})


class SalesPipelineViewSet(viewsets.ModelViewSet):
    queryset = SalesPipeline.objects.all()
    serializer_class = SalesPipelineSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'created_by']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


class SalesForecastViewSet(viewsets.ModelViewSet):
    queryset = SalesForecast.objects.all()
    serializer_class = SalesForecastSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['forecast_period', 'forecast_type', 'assigned_to']
    search_fields = ['title', 'description']
    ordering_fields = ['forecast_date', 'created_at']
    ordering = ['-forecast_date', '-created_at']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get sales forecast summary"""
        total_forecast = sum(forecast.forecasted_amount for forecast in self.get_queryset())
        return Response({
            'total_forecasted_amount': total_forecast,
            'forecast_count': self.get_queryset().count()
        })
