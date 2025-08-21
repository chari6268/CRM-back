from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg, Count, Sum
from .models import (
    ChurnRisk, CustomerMetrics, SentimentAnalysis, ProductFeedback
)
from .serializers import (
    ChurnRiskSerializer, CustomerMetricsSerializer, SentimentAnalysisSerializer,
    ProductFeedbackSerializer
)


class ChurnRiskViewSet(viewsets.ModelViewSet):
    queryset = ChurnRisk.objects.all()
    serializer_class = ChurnRiskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['risk_level', 'customer', 'last_calculated']
    search_fields = ['customer__full_name']
    ordering_fields = ['risk_score', 'last_calculated', 'created_at']
    ordering = ['-risk_score', '-last_calculated']

    @action(detail=False, methods=['get'])
    def high_risk_customers(self, request):
        """Get customers with high churn risk"""
        high_risk = self.get_queryset().filter(risk_level__in=['high', 'critical'])
        serializer = self.get_serializer(high_risk, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def risk_distribution(self, request):
        """Get churn risk distribution"""
        distribution = self.get_queryset().values('risk_level').annotate(
            count=Count('id')
        ).order_by('risk_level')
        return Response(distribution)


class CustomerMetricsViewSet(viewsets.ModelViewSet):
    queryset = CustomerMetrics.objects.all()
    serializer_class = CustomerMetricsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['customer', 'date']
    search_fields = ['customer__full_name']
    ordering_fields = ['date', 'satisfaction_score', 'revenue', 'created_at']
    ordering = ['-date']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get customer metrics summary"""
        total_customers = self.get_queryset().values('customer').distinct().count()
        avg_satisfaction = self.get_queryset().aggregate(
            avg_satisfaction=Avg('satisfaction_score')
        )['avg_satisfaction'] or 0
        total_revenue = self.get_queryset().aggregate(
            total_revenue=Sum('revenue')
        )['total_revenue'] or 0
        
        return Response({
            'total_customers': total_customers,
            'average_satisfaction': avg_satisfaction,
            'total_revenue': total_revenue
        })


class SentimentAnalysisViewSet(viewsets.ModelViewSet):
    queryset = SentimentAnalysis.objects.all()
    serializer_class = SentimentAnalysisSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['customer', 'source', 'sentiment']
    search_fields = ['customer__full_name', 'text_content']
    ordering_fields = ['confidence_score', 'date', 'created_at']
    ordering = ['-date']

    @action(detail=False, methods=['get'])
    def sentiment_summary(self, request):
        """Get sentiment analysis summary"""
        sentiment_counts = self.get_queryset().values('sentiment').annotate(
            count=Count('id')
        ).order_by('sentiment')
        
        avg_confidence = self.get_queryset().aggregate(
            avg_confidence=Avg('confidence_score')
        )['avg_confidence'] or 0
        
        return Response({
            'sentiment_distribution': sentiment_counts,
            'average_confidence': avg_confidence
        })


class ProductFeedbackViewSet(viewsets.ModelViewSet):
    queryset = ProductFeedback.objects.all()
    serializer_class = ProductFeedbackSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['customer', 'type', 'priority']
    search_fields = ['title', 'description', 'customer__full_name']
    ordering_fields = ['priority', 'rating', 'created_at']
    ordering = ['-priority', '-created_at']

    @action(detail=False, methods=['get'])
    def feedback_summary(self, request):
        """Get product feedback summary"""
        feedback_counts = self.get_queryset().values('type').annotate(
            count=Count('id')
        ).order_by('type')
        
        priority_counts = self.get_queryset().values('priority').annotate(
            count=Count('id')
        ).order_by('priority')
        
        avg_rating = self.get_queryset().aggregate(
            avg_rating=Avg('rating')
        )['avg_rating'] or 0
        
        return Response({
            'feedback_by_type': feedback_counts,
            'feedback_by_priority': priority_counts,
            'average_rating': avg_rating
        })
