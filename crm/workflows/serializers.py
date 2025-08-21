from rest_framework import serializers
from .models import (
    WorkflowDefinition, WorkflowStep, WorkflowExecution, WorkflowStepExecution,
    WorkflowTemplate, WorkflowVariable, WorkflowIntegration, WorkflowMetrics
)
from crm.core.serializers import UserSerializer


class WorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowStep
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class WorkflowVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowVariable
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class WorkflowDefinitionSerializer(serializers.ModelSerializer):
    steps = WorkflowStepSerializer(many=True, read_only=True)
    variables = WorkflowVariableSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = WorkflowDefinition
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkflowStepExecutionSerializer(serializers.ModelSerializer):
    step = WorkflowStepSerializer(read_only=True)
    
    class Meta:
        model = WorkflowStepExecution
        fields = '__all__'
        read_only_fields = ['id', 'started_at', 'completed_at', 'created_at']


class WorkflowExecutionSerializer(serializers.ModelSerializer):
    workflow = WorkflowDefinitionSerializer(read_only=True)
    step_executions = WorkflowStepExecutionSerializer(many=True, read_only=True)
    
    class Meta:
        model = WorkflowExecution
        fields = '__all__'
        read_only_fields = ['id', 'execution_id', 'started_at', 'completed_at', 'created_at']


class WorkflowTemplateSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = WorkflowTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkflowIntegrationSerializer(serializers.ModelSerializer):
    workflow = WorkflowDefinitionSerializer(read_only=True)
    
    class Meta:
        model = WorkflowIntegration
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkflowMetricsSerializer(serializers.ModelSerializer):
    workflow = WorkflowDefinitionSerializer(read_only=True)
    
    class Meta:
        model = WorkflowMetrics
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
