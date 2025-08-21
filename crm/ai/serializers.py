from rest_framework import serializers
from .models import (
    AIModel, PredictiveScore, Chatbot, ChatbotConversation, ChatbotMessage,
    PersonalizationRule, AIRecommendation, AITrainingData, AIModelPerformance
)
from crm.core.serializers import UserSerializer, CustomerSerializer


class AIModelSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = AIModel
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_trained']


class PredictiveScoreSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    ai_model = AIModelSerializer(read_only=True)
    
    class Meta:
        model = PredictiveScore
        fields = '__all__'
        read_only_fields = ['id', 'calculated_at']


class ChatbotSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Chatbot
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class ChatbotMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotMessage
        fields = '__all__'
        read_only_fields = ['id', 'timestamp', 'created_at']


class ChatbotConversationSerializer(serializers.ModelSerializer):
    chatbot = ChatbotSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    messages = ChatbotMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatbotConversation
        fields = '__all__'
        read_only_fields = ['id', 'session_id', 'started_at', 'ended_at', 'created_at']


class PersonalizationRuleSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = PersonalizationRule
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class AIRecommendationSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    ai_model = AIModelSerializer(read_only=True)
    
    class Meta:
        model = AIRecommendation
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'implemented_at']


class AITrainingDataSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = AITrainingData
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class AIModelPerformanceSerializer(serializers.ModelSerializer):
    ai_model = AIModelSerializer(read_only=True)
    
    class Meta:
        model = AIModelPerformance
        fields = '__all__'
        read_only_fields = ['id', 'evaluation_date', 'created_at']
