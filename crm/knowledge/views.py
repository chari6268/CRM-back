from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    KnowledgeCategory, KnowledgeArticle, KnowledgeTag, KnowledgeComment,
    KnowledgeFeedback, KnowledgeSearch, KnowledgeTemplate, KnowledgeAnalytics,
    KnowledgeVersion
)
from .serializers import (
    KnowledgeCategorySerializer, KnowledgeArticleSerializer, KnowledgeTagSerializer,
    KnowledgeCommentSerializer, KnowledgeFeedbackSerializer, KnowledgeSearchSerializer,
    KnowledgeTemplateSerializer, KnowledgeAnalyticsSerializer, KnowledgeVersionSerializer
)
from django.utils import timezone


class KnowledgeCategoryViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeCategory.objects.all()
    serializer_class = KnowledgeCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['company', 'is_active', 'parent_category']
    search_fields = ['name', 'description']
    ordering_fields = ['order', 'created_at']
    ordering = ['order', 'name']


class KnowledgeTagViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeTag.objects.all()
    serializer_class = KnowledgeTagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['company']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class KnowledgeArticleViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeArticle.objects.all()
    serializer_class = KnowledgeArticleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'status', 'article_type', 'company', 'author', 'is_public']
    search_fields = ['title', 'content', 'summary', 'keywords']
    ordering_fields = ['created_at', 'updated_at', 'published_at', 'views_count']
    ordering = ['-published_at', '-created_at']

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        article = self.get_object()
        article.status = 'published'
        article.published_at = timezone.now()
        article.save()
        return Response({'status': 'Article published'})

    @action(detail=True, methods=['post'])
    def increment_view(self, request, pk=None):
        article = self.get_object()
        article.views_count += 1
        article.save()
        return Response({'status': 'View count incremented'})


class KnowledgeCommentViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeComment.objects.all()
    serializer_class = KnowledgeCommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['article', 'author', 'is_approved', 'parent_comment']
    search_fields = ['content']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        comment = self.get_object()
        comment.is_approved = True
        comment.save()
        return Response({'status': 'Comment approved'})


class KnowledgeFeedbackViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeFeedback.objects.all()
    serializer_class = KnowledgeFeedbackSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['article', 'user', 'feedback_type', 'rating']
    search_fields = ['comment']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-rating', '-created_at']


class KnowledgeSearchViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeSearch.objects.all()
    serializer_class = KnowledgeSearchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['company', 'clicked_article']
    search_fields = ['query']
    ordering_fields = ['search_time', 'created_at']
    ordering = ['-search_time']


class KnowledgeTemplateViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeTemplate.objects.all()
    serializer_class = KnowledgeTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_active', 'company', 'created_by']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


class KnowledgeAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeAnalytics.objects.all()
    serializer_class = KnowledgeAnalyticsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['article', 'date']
    search_fields = ['article__title']
    ordering_fields = ['date', 'views', 'created_at']
    ordering = ['-date']


class KnowledgeVersionViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeVersion.objects.all()
    serializer_class = KnowledgeVersionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['article', 'version_number', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['version_number', 'created_at']
    ordering = ['-version_number']
