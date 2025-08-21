from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    Survey, SurveyQuestion, SurveyResponse, SurveyAnswer, NPSScore,
    SurveyTemplate, SurveyMetrics
)
from .serializers import (
    SurveySerializer, SurveyQuestionSerializer, SurveyResponseSerializer,
    SurveyAnswerSerializer, NPSScoreSerializer, SurveyTemplateSerializer,
    SurveyMetricsSerializer
)
from django.utils import timezone


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['survey_type', 'is_active', 'company', 'created_by']
    search_fields = ['title', 'description']
    ordering_fields = ['start_date', 'end_date', 'created_at']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        survey = self.get_object()
        survey.is_active = True
        survey.save()
        return Response({'status': 'Survey activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        survey = self.get_object()
        survey.is_active = False
        survey.save()
        return Response({'status': 'Survey deactivated'})


class SurveyQuestionViewSet(viewsets.ModelViewSet):
    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['survey', 'question_type', 'is_required']
    search_fields = ['question_text']
    ordering_fields = ['order', 'created_at']
    ordering = ['survey', 'order']


class SurveyResponseViewSet(viewsets.ModelViewSet):
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['survey', 'customer', 'is_completed']
    search_fields = ['respondent_email', 'respondent_name']
    ordering_fields = ['started_at', 'completed_at', 'created_at']
    ordering = ['-started_at']

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        response = self.get_object()
        response.is_completed = True
        response.completed_at = timezone.now()
        response.save()
        return Response({'status': 'Survey completed'})


class SurveyAnswerViewSet(viewsets.ModelViewSet):
    queryset = SurveyAnswer.objects.all()
    serializer_class = SurveyAnswerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['response', 'question']
    search_fields = ['answer_text']
    ordering_fields = ['created_at']
    ordering = ['response', 'question__order']


class NPSScoreViewSet(viewsets.ModelViewSet):
    queryset = NPSScore.objects.all()
    serializer_class = NPSScoreSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['customer', 'company', 'score']
    search_fields = ['customer__name']
    ordering_fields = ['score', 'created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get NPS summary statistics"""
        promoters = self.get_queryset().filter(score__gte=9).count()
        passives = self.get_queryset().filter(score__in=[7, 8]).count()
        detractors = self.get_queryset().filter(score__lte=6).count()
        total = promoters + passives + detractors
        
        nps_score = ((promoters - detractors) / total * 100) if total > 0 else 0
        
        return Response({
            'total_responses': total,
            'promoters': promoters,
            'passives': passives,
            'detractors': detractors,
            'nps_score': nps_score
        })


class SurveyTemplateViewSet(viewsets.ModelViewSet):
    queryset = SurveyTemplate.objects.all()
    serializer_class = SurveyTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['survey_type', 'is_public', 'company', 'created_by']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


class SurveyMetricsViewSet(viewsets.ModelViewSet):
    queryset = SurveyMetrics.objects.all()
    serializer_class = SurveyMetricsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['survey', 'last_calculated']
    search_fields = ['survey__title']
    ordering_fields = ['last_calculated', 'created_at']
    ordering = ['-last_calculated']
