from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    AIModel, PredictiveScore, Chatbot, ChatbotConversation, ChatbotMessage,
    PersonalizationRule, AIRecommendation, AITrainingData, AIModelPerformance
)
from .serializers import (
    AIModelSerializer, PredictiveScoreSerializer, ChatbotSerializer,
    ChatbotConversationSerializer, ChatbotMessageSerializer, PersonalizationRuleSerializer,
    AIRecommendationSerializer, AITrainingDataSerializer, AIModelPerformanceSerializer
)
from django.db.models import Avg
from django.utils import timezone


class AIModelViewSet(viewsets.ModelViewSet):
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['model_type', 'status', 'created_by']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'last_trained']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def train(self, request, pk=None):
        model = self.get_object()
        model.status = 'training'
        model.save()
        # Here you would implement the actual training logic
        return Response({'status': 'Training started'})

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        model = self.get_object()
        model.status = 'active'
        model.save()
        return Response({'status': 'Model activated'})


class PredictiveScoreViewSet(viewsets.ModelViewSet):
    queryset = PredictiveScore.objects.all()
    serializer_class = PredictiveScoreSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['score_type', 'customer', 'ai_model']
    search_fields = ['customer__name']
    ordering_fields = ['score_value', 'confidence_level', 'calculated_at']
    ordering = ['-calculated_at']

    @action(detail=False, methods=['get'])
    def high_risk_customers(self, request):
        """Get customers with high risk scores"""
        high_risk_scores = self.get_queryset().filter(score_value__gte=80)
        serializer = self.get_serializer(high_risk_scores, many=True)
        return Response(serializer.data)


class ChatbotViewSet(viewsets.ModelViewSet):
    queryset = Chatbot.objects.all()
    serializer_class = ChatbotSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['bot_type', 'platform', 'is_active', 'created_by']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        chatbot = self.get_object()
        chatbot.is_active = True
        chatbot.save()
        return Response({'status': 'Chatbot activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        chatbot = self.get_object()
        chatbot.is_active = False
        chatbot.save()
        return Response({'status': 'Chatbot deactivated'})


class ChatbotConversationViewSet(viewsets.ModelViewSet):
    queryset = ChatbotConversation.objects.all()
    serializer_class = ChatbotConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['chatbot', 'customer', 'status']
    search_fields = ['session_id']
    ordering_fields = ['started_at', 'ended_at', 'created_at']
    ordering = ['-started_at']


class ChatbotMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatbotMessage.objects.all()
    serializer_class = ChatbotMessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['conversation', 'message_type', 'sender_type']
    search_fields = ['content']
    ordering_fields = ['timestamp', 'created_at']
    ordering = ['conversation', 'timestamp']


class PersonalizationRuleViewSet(viewsets.ModelViewSet):
    queryset = PersonalizationRule.objects.all()
    serializer_class = PersonalizationRuleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['rule_type', 'is_active', 'created_by']
    search_fields = ['name', 'description']
    ordering_fields = ['priority', 'created_at', 'updated_at']
    ordering = ['priority', '-created_at']

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        rule = self.get_object()
        rule.is_active = True
        rule.save()
        return Response({'status': 'Rule activated'})


class AIRecommendationViewSet(viewsets.ModelViewSet):
    queryset = AIRecommendation.objects.all()
    serializer_class = AIRecommendationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['recommendation_type', 'customer', 'ai_model', 'is_implemented']
    search_fields = ['title', 'description']
    ordering_fields = ['confidence_score', 'created_at']
    ordering = ['-confidence_score', '-created_at']

    @action(detail=True, methods=['post'])
    def implement(self, request, pk=None):
        recommendation = self.get_object()
        recommendation.is_implemented = True
        recommendation.implemented_at = timezone.now()
        recommendation.save()
        return Response({'status': 'Recommendation implemented'})


class AITrainingDataViewSet(viewsets.ModelViewSet):
    queryset = AITrainingData.objects.all()
    serializer_class = AITrainingDataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['data_type', 'source', 'quality_score', 'is_processed']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'quality_score']
    ordering = ['-created_at']


class AIModelPerformanceViewSet(viewsets.ModelViewSet):
    queryset = AIModelPerformance.objects.all()
    serializer_class = AIModelPerformanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ai_model', 'metric_type', 'evaluation_date']
    search_fields = ['ai_model__name']
    ordering_fields = ['evaluation_date', 'metric_value', 'created_at']
    ordering = ['-evaluation_date', '-metric_value']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get AI model performance summary"""
        total_models = self.get_queryset().values('ai_model').distinct().count()
        avg_accuracy = self.get_queryset().filter(metric_type='accuracy').aggregate(
            avg_value=Avg('metric_value')
        )['avg_value'] or 0
        
        return Response({
            'total_models': total_models,
            'average_accuracy': avg_accuracy
        })
