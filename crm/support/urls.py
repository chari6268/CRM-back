from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tickets', views.SupportTicketViewSet)
router.register(r'responses', views.TicketResponseViewSet)
router.register(r'slas', views.ServiceLevelAgreementViewSet)
router.register(r'knowledge', views.KnowledgeBaseViewSet)
router.register(r'feedback', views.CustomerFeedbackViewSet)
router.register(r'team', views.SupportTeamViewSet)
router.register(r'metrics', views.SupportMetricsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
