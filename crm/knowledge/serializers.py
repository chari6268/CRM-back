from rest_framework import serializers
from .models import (
    KnowledgeCategory, KnowledgeArticle, KnowledgeTag, KnowledgeComment,
    KnowledgeFeedback, KnowledgeSearch, KnowledgeTemplate, KnowledgeAnalytics,
    KnowledgeVersion
)
from crm.core.serializers import UserSerializer, CompanySerializer


class KnowledgeCategorySerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    parent_category = 'self'  # Self-referencing relationship
    subcategories = serializers.SerializerMethodField()
    
    class Meta:
        model = KnowledgeCategory
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_subcategories(self, obj):
        if obj.subcategories.exists():
            return KnowledgeCategorySerializer(obj.subcategories.all(), many=True).data
        return []


class KnowledgeTagSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    
    class Meta:
        model = KnowledgeTag
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class KnowledgeCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    parent_comment = 'self'  # Self-referencing relationship
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = KnowledgeComment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return KnowledgeCommentSerializer(obj.replies.all(), many=True).data
        return []


class KnowledgeArticleSerializer(serializers.ModelSerializer):
    category = KnowledgeCategorySerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    author = UserSerializer(read_only=True)
    reviewed_by = UserSerializer(read_only=True)
    tags = KnowledgeTagSerializer(many=True, read_only=True)
    related_articles = 'self'  # Self-referencing relationship
    comments = KnowledgeCommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = KnowledgeArticle
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'published_at', 'last_reviewed', 'views_count', 'helpful_votes', 'not_helpful_votes']


class KnowledgeFeedbackSerializer(serializers.ModelSerializer):
    article = KnowledgeArticleSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = KnowledgeFeedback
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class KnowledgeSearchSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    clicked_article = KnowledgeArticleSerializer(read_only=True)
    
    class Meta:
        model = KnowledgeSearch
        fields = '__all__'
        read_only_fields = ['id', 'search_time', 'created_at']


class KnowledgeTemplateSerializer(serializers.ModelSerializer):
    category = KnowledgeCategorySerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = KnowledgeTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class KnowledgeAnalyticsSerializer(serializers.ModelSerializer):
    article = KnowledgeArticleSerializer(read_only=True)
    
    class Meta:
        model = KnowledgeAnalytics
        fields = '__all__'
        read_only_fields = ['id', 'date', 'created_at']


class KnowledgeVersionSerializer(serializers.ModelSerializer):
    article = KnowledgeArticleSerializer(read_only=True)
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = KnowledgeVersion
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
