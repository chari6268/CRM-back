from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from crm.core.models import Customer, Company
import uuid

class WorkflowDefinition(models.Model):
    """Workflow definitions and templates"""
    WORKFLOW_TYPES = [
        ('customer_onboarding', 'Customer Onboarding'),
        ('lead_nurturing', 'Lead Nurturing'),
        ('support_escalation', 'Support Escalation'),
        ('approval_process', 'Approval Process'),
        ('data_sync', 'Data Synchronization'),
        ('notification', 'Notification Workflow'),
        ('custom', 'Custom Workflow'),
    ]
    
    TRIGGER_TYPES = [
        ('event_based', 'Event Based'),
        ('time_based', 'Time Based'),
        ('manual', 'Manual Trigger'),
        ('webhook', 'Webhook'),
        ('api_call', 'API Call'),
        ('condition_based', 'Condition Based'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    workflow_type = models.CharField(max_length=30, choices=WORKFLOW_TYPES)
    trigger_type = models.CharField(max_length=20, choices=TRIGGER_TYPES)
    trigger_conditions = models.JSONField(default=dict)  # Trigger conditions
    workflow_steps = models.JSONField(default=list)  # Workflow steps configuration
    variables = models.JSONField(default=dict)  # Workflow variables
    is_active = models.BooleanField(default=True)
    is_template = models.BooleanField(default=False)
    version = models.CharField(max_length=20, default='1.0.0')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_workflows')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} v{self.version}"

class WorkflowStep(models.Model):
    """Individual workflow steps and actions"""
    STEP_TYPES = [
        ('action', 'Action'),
        ('condition', 'Condition'),
        ('delay', 'Delay'),
        ('webhook', 'Webhook'),
        ('email', 'Send Email'),
        ('notification', 'Send Notification'),
        ('task', 'Create Task'),
        ('data_update', 'Update Data'),
        ('approval', 'Approval'),
        ('integration', 'Integration'),
        ('custom', 'Custom Action'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(WorkflowDefinition, on_delete=models.CASCADE, related_name='steps')
    name = models.CharField(max_length=200)
    step_type = models.CharField(max_length=20, choices=STEP_TYPES)
    order = models.IntegerField()
    configuration = models.JSONField(default=dict)  # Step-specific configuration
    conditions = models.JSONField(default=dict)  # Step execution conditions
    next_steps = models.JSONField(default=list)  # Next step logic
    is_required = models.BooleanField(default=True)
    timeout = models.IntegerField(null=True, blank=True, help_text='Timeout in seconds')
    retry_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['workflow', 'order']
        unique_together = ['workflow', 'order']
    
    def __str__(self):
        return f"{self.workflow.name} - Step {self.order}: {self.name}"

class WorkflowExecution(models.Model):
    """Workflow execution instances"""
    EXECUTION_STATUS = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('paused', 'Paused'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(WorkflowDefinition, on_delete=models.CASCADE, related_name='executions')
    execution_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=EXECUTION_STATUS, default='pending')
    trigger_data = models.JSONField(default=dict)  # Data that triggered the workflow
    context_data = models.JSONField(default=dict)  # Workflow execution context
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='triggered_workflows')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.workflow.name} - {self.execution_id}"

class WorkflowStepExecution(models.Model):
    """Individual step execution tracking"""
    STEP_STATUS = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('skipped', 'Skipped'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow_execution = models.ForeignKey(WorkflowExecution, on_delete=models.CASCADE, related_name='step_executions')
    workflow_step = models.ForeignKey(WorkflowStep, on_delete=models.CASCADE, related_name='executions')
    status = models.CharField(max_length=20, choices=STEP_STATUS, default='pending')
    input_data = models.JSONField(default=dict)  # Input data for the step
    output_data = models.JSONField(default=dict)  # Output data from the step
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, help_text='Duration in seconds')
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['workflow_execution', 'workflow_step__order']
    
    def __str__(self):
        return f"{self.workflow_execution.execution_id} - {self.workflow_step.name}"

class WorkflowTemplate(models.Model):
    """Pre-built workflow templates for common use cases"""
    CATEGORIES = [
        ('sales', 'Sales'),
        ('marketing', 'Marketing'),
        ('support', 'Support'),
        ('onboarding', 'Onboarding'),
        ('offboarding', 'Offboarding'),
        ('approval', 'Approval'),
        ('notification', 'Notification'),
        ('integration', 'Integration'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    template_data = models.JSONField(default=dict)  # Template configuration
    is_public = models.BooleanField(default=True)
    usage_count = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_templates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-usage_count', '-rating']
    
    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

class WorkflowVariable(models.Model):
    """Workflow variables and their definitions"""
    VARIABLE_TYPES = [
        ('string', 'String'),
        ('number', 'Number'),
        ('boolean', 'Boolean'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
        ('json', 'JSON'),
        ('array', 'Array'),
        ('object', 'Object'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(WorkflowDefinition, on_delete=models.CASCADE, related_name='workflow_variables')
    name = models.CharField(max_length=100)
    variable_type = models.CharField(max_length=20, choices=VARIABLE_TYPES)
    description = models.TextField(blank=True)
    default_value = models.TextField(blank=True)
    is_required = models.BooleanField(default=False)
    validation_rules = models.JSONField(default=dict)  # Validation rules
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['workflow', 'name']
        unique_together = ['workflow', 'name']
    
    def __str__(self):
        return f"{self.workflow.name} - {self.name}"

class WorkflowIntegration(models.Model):
    """External integrations for workflows"""
    INTEGRATION_TYPES = [
        ('api', 'API Integration'),
        ('webhook', 'Webhook'),
        ('email', 'Email Service'),
        ('sms', 'SMS Service'),
        ('slack', 'Slack'),
        ('teams', 'Microsoft Teams'),
        ('zapier', 'Zapier'),
        ('make', 'Make (Integromat)'),
        ('custom', 'Custom Integration'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    integration_type = models.CharField(max_length=20, choices=INTEGRATION_TYPES)
    description = models.TextField(blank=True)
    configuration = models.JSONField(default=dict)  # Integration configuration
    credentials = models.JSONField(default=dict)  # Encrypted credentials
    is_active = models.BooleanField(default=True)
    test_status = models.CharField(max_length=20, default='untested')
    last_tested = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_integrations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_integration_type_display()}"

class WorkflowMetrics(models.Model):
    """Workflow performance metrics and analytics"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(WorkflowDefinition, on_delete=models.CASCADE, related_name='metrics')
    date = models.DateField()
    total_executions = models.IntegerField(default=0)
    successful_executions = models.IntegerField(default=0)
    failed_executions = models.IntegerField(default=0)
    avg_execution_time = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # In seconds
    total_steps_executed = models.IntegerField(default=0)
    avg_steps_per_execution = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['workflow', 'date']
    
    def __str__(self):
        return f"{self.workflow.name} Metrics - {self.date}"
