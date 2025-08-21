from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'definitions', views.WorkflowDefinitionViewSet)
router.register(r'steps', views.WorkflowStepViewSet)
router.register(r'executions', views.WorkflowExecutionViewSet)
router.register(r'step-executions', views.WorkflowStepExecutionViewSet)
router.register(r'templates', views.WorkflowTemplateViewSet)
router.register(r'variables', views.WorkflowVariableViewSet)
router.register(r'integrations', views.WorkflowIntegrationViewSet)
router.register(r'metrics', views.WorkflowMetricsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
