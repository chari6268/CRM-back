from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'models', views.AIModelViewSet)
router.register(r'predictive-scores', views.PredictiveScoreViewSet)
router.register(r'chatbots', views.ChatbotViewSet)
router.register(r'conversations', views.ChatbotConversationViewSet)
router.register(r'messages', views.ChatbotMessageViewSet)
router.register(r'personalization-rules', views.PersonalizationRuleViewSet)
router.register(r'recommendations', views.AIRecommendationViewSet)
router.register(r'training-data', views.AITrainingDataViewSet)
router.register(r'performance', views.AIModelPerformanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
