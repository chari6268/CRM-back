from rest_framework import serializers
from .models import (
    Survey, SurveyQuestion, SurveyResponse, SurveyAnswer, NPSScore,
    SurveyTemplate, SurveyMetrics
)
from crm.core.serializers import UserSerializer, CompanySerializer, CustomerSerializer


class SurveyQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestion
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class SurveyAnswerSerializer(serializers.ModelSerializer):
    question = SurveyQuestionSerializer(read_only=True)
    
    class Meta:
        model = SurveyAnswer
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class SurveyResponseSerializer(serializers.ModelSerializer):
    survey = SurveySerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    answers = SurveyAnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = SurveyResponse
        fields = '__all__'
        read_only_fields = ['id', 'started_at', 'completed_at']


class SurveySerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    questions = SurveyQuestionSerializer(many=True, read_only=True)
    responses = SurveyResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Survey
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class NPSScoreSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    survey_response = SurveyResponseSerializer(read_only=True)
    
    class Meta:
        model = NPSScore
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class SurveyTemplateSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = SurveyTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class SurveyMetricsSerializer(serializers.ModelSerializer):
    survey = SurveySerializer(read_only=True)
    
    class Meta:
        model = SurveyMetrics
        fields = '__all__'
        read_only_fields = ['id', 'last_calculated']
