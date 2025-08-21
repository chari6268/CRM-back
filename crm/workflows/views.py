from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import (
    WorkflowDefinition, WorkflowStep, WorkflowExecution, WorkflowStepExecution,
    WorkflowTemplate, WorkflowVariable, WorkflowIntegration, WorkflowMetrics
)
from .serializers import (
    WorkflowDefinitionSerializer, WorkflowStepSerializer, WorkflowExecutionSerializer,
    WorkflowStepExecutionSerializer, WorkflowTemplateSerializer, WorkflowVariableSerializer,
    WorkflowIntegrationSerializer, WorkflowMetricsSerializer
)


class WorkflowDefinitionViewSet(viewsets.ModelViewSet):
    queryset = WorkflowDefinition.objects.all()
    serializer_class = WorkflowDefinitionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['workflow_type', 'trigger_type', 'is_active', 'is_template', 'created_by']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'version']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        workflow = self.get_object()
        workflow.is_active = True
        workflow.save()
        return Response({'status': 'Workflow activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        workflow = self.get_object()
        workflow.is_active = False
        workflow.save()
        return Response({'status': 'Workflow deactivated'})


class WorkflowStepViewSet(viewsets.ModelViewSet):
    queryset = WorkflowStep.objects.all()
    serializer_class = WorkflowStepSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['workflow', 'step_type', 'is_required']
    search_fields = ['name']
    ordering_fields = ['order', 'created_at']
    ordering = ['workflow', 'order']


class WorkflowExecutionViewSet(viewsets.ModelViewSet):
    queryset = WorkflowExecution.objects.all()
    serializer_class = WorkflowExecutionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['workflow', 'status', 'execution_id']
    search_fields = ['execution_id']
    ordering_fields = ['started_at', 'completed_at', 'created_at']
    ordering = ['-started_at']

    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        execution = self.get_object()
        execution.status = 'paused'
        execution.save()
        return Response({'status': 'Execution paused'})

    @action(detail=True, methods=['post'])
    def resume(self, request, pk=None):
        execution = self.get_object()
        execution.status = 'running'
        execution.save()
        return Response({'status': 'Execution resumed'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        execution = self.get_object()
        execution.status = 'cancelled'
        execution.save()
        return Response({'status': 'Execution cancelled'})


class WorkflowStepExecutionViewSet(viewsets.ModelViewSet):
    queryset = WorkflowStepExecution.objects.all()
    serializer_class = WorkflowStepExecutionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['execution', 'step', 'status']
    search_fields = ['step__name']
    ordering_fields = ['started_at', 'completed_at', 'created_at']
    ordering = ['execution', 'step__order']


class WorkflowTemplateViewSet(viewsets.ModelViewSet):
    queryset = WorkflowTemplate.objects.all()
    serializer_class = WorkflowTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['template_type', 'is_active', 'created_by']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


class WorkflowVariableViewSet(viewsets.ModelViewSet):
    queryset = WorkflowVariable.objects.all()
    serializer_class = WorkflowVariableSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['workflow', 'variable_type', 'is_required']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at']
    ordering = ['workflow', 'name']


class WorkflowIntegrationViewSet(viewsets.ModelViewSet):
    queryset = WorkflowIntegration.objects.all()
    serializer_class = WorkflowIntegrationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['workflow', 'integration_type', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


class WorkflowMetricsViewSet(viewsets.ModelViewSet):
    queryset = WorkflowMetrics.objects.all()
    serializer_class = WorkflowMetricsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['workflow', 'date', 'metric_type']
    search_fields = ['workflow__name']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date', '-created_at']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get workflow metrics summary"""
        total_executions = sum(metric.total_executions for metric in self.get_queryset())
        successful_executions = sum(metric.successful_executions for metric in self.get_queryset())
        failed_executions = sum(metric.failed_executions for metric in self.get_queryset())
        
        return Response({
            'total_executions': total_executions,
            'successful_executions': successful_executions,
            'failed_executions': failed_executions,
            'success_rate': (successful_executions / total_executions * 100) if total_executions > 0 else 0
        })
