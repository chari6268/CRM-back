from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from crm.core.models import Customer, Company
import uuid

class SupportTicket(models.Model):
    """Customer support ticket management"""
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
        ('critical', 'Critical'),
    ]
    
    TICKET_STATUS = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('waiting_customer', 'Waiting for Customer'),
        ('waiting_third_party', 'Waiting for Third Party'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ]
    
    TICKET_TYPES = [
        ('bug', 'Bug Report'),
        ('feature_request', 'Feature Request'),
        ('technical_support', 'Technical Support'),
        ('billing', 'Billing Issue'),
        ('account', 'Account Issue'),
        ('general', 'General Inquiry'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='support_tickets')
    title = models.CharField(max_length=200)
    description = models.TextField()
    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPES)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')
    status = models.CharField(max_length=20, choices=TICKET_STATUS, default='open')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    tags = models.JSONField(default=list)
    
    class Meta:
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.ticket_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if self.status in ['resolved', 'closed'] and not self.resolved_at:
            self.resolved_at = timezone.now()
        if self.status == 'closed' and not self.closed_at:
            self.closed_at = timezone.now()
        super().save(*args, **kwargs)

class TicketResponse(models.Model):
    """Ticket responses and communication history"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ticket_responses')
    message = models.TextField()
    is_internal = models.BooleanField(default=False)  # Internal note vs customer response
    attachments = models.JSONField(default=list)  # File attachments
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Response to {self.ticket.ticket_number} by {self.user.username if self.user else 'System'}"

class ServiceLevelAgreement(models.Model):
    """Service Level Agreements for support tickets"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20, choices=SupportTicket.PRIORITY_LEVELS)
    response_time = models.IntegerField(help_text='Response time in hours')
    resolution_time = models.IntegerField(help_text='Resolution time in hours')
    business_hours = models.JSONField(default=dict)  # Business hours configuration
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['priority', 'response_time']
        unique_together = ['priority', 'is_active']
    
    def __str__(self):
        return f"{self.name} - {self.get_priority_display()}"

class KnowledgeBase(models.Model):
    """Knowledge base articles and documentation"""
    ARTICLE_TYPES = [
        ('how_to', 'How-to Guide'),
        ('troubleshooting', 'Troubleshooting'),
        ('faq', 'FAQ'),
        ('tutorial', 'Tutorial'),
        ('reference', 'Reference'),
        ('announcement', 'Announcement'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    article_type = models.CharField(max_length=20, choices=ARTICLE_TYPES)
    category = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    helpful_count = models.IntegerField(default=0)
    not_helpful_count = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='knowledge_articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title

class CustomerFeedback(models.Model):
    """Customer feedback and satisfaction ratings"""
    FEEDBACK_TYPES = [
        ('ticket', 'Support Ticket'),
        ('knowledge', 'Knowledge Base'),
        ('general', 'General'),
        ('product', 'Product'),
        ('service', 'Service'),
    ]
    
    RATING_CHOICES = [
        (1, 'Very Dissatisfied'),
        (2, 'Dissatisfied'),
        (3, 'Neutral'),
        (4, 'Satisfied'),
        (5, 'Very Satisfied'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='feedback')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback')
    knowledge_article = models.ForeignKey(KnowledgeBase, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback from {self.customer.name} - {self.get_rating_display()}"

class SupportTeam(models.Model):
    """Support team management and skills"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='support_profile')
    skills = models.JSONField(default=list)  # Technical skills
    specializations = models.JSONField(default=list)  # Areas of expertise
    max_tickets = models.IntegerField(default=10, help_text='Maximum concurrent tickets')
    is_available = models.BooleanField(default=True)
    working_hours = models.JSONField(default=dict)  # Working hours
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Support Profile for {self.user.username}"

class SupportMetrics(models.Model):
    """Support performance metrics and KPIs"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    total_tickets = models.IntegerField(default=0)
    resolved_tickets = models.IntegerField(default=0)
    avg_response_time = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # In hours
    avg_resolution_time = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # In hours
    customer_satisfaction = models.DecimalField(max_digits=3, decimal_places=2, default=0)  # Average rating
    first_call_resolution = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Percentage
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['date']
    
    def __str__(self):
        return f"Support Metrics for {self.date}"
