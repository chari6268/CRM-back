from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from crm.core.models import Customer, Company
import uuid

class Lead(models.Model):
    """Lead management with scoring and qualification"""
    LEAD_STATUS = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('unqualified', 'Unqualified'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]
    
    LEAD_SOURCE = [
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('social_media', 'Social Media'),
        ('cold_call', 'Cold Call'),
        ('email_campaign', 'Email Campaign'),
        ('trade_show', 'Trade Show'),
        ('advertising', 'Advertising'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=100, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(max_length=50, blank=True)
    lead_source = models.CharField(max_length=20, choices=LEAD_SOURCE)
    status = models.CharField(max_length=20, choices=LEAD_STATUS, default='new')
    lead_score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    timeline = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_leads')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_leads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_contacted = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-lead_score', '-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Opportunity(models.Model):
    """Sales opportunities with pipeline management"""
    OPPORTUNITY_STAGES = [
        ('prospecting', 'Prospecting'),
        ('qualification', 'Qualification'),
        ('needs_analysis', 'Needs Analysis'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name='opportunities')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='opportunities')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    stage = models.CharField(max_length=20, choices=OPPORTUNITY_STAGES, default='prospecting')
    probability = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    expected_close_date = models.DateField()
    actual_close_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_opportunities')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_opportunities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-expected_close_date', '-amount']
        verbose_name_plural = 'Opportunities'
    
    def __str__(self):
        return f"{self.title} - {self.customer.name}"

class Deal(models.Model):
    """Closed deals with revenue tracking"""
    DEAL_STATUS = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    opportunity = models.OneToOneField(Opportunity, on_delete=models.CASCADE, related_name='deal')
    deal_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=DEAL_STATUS, default='pending')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    start_date = models.DateField()
    end_date = models.DateField()
    payment_terms = models.CharField(max_length=100, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_deals')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.deal_number} - {self.title}"

class SalesActivity(models.Model):
    """Track all sales activities and touchpoints"""
    ACTIVITY_TYPES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('demo', 'Product Demo'),
        ('proposal', 'Proposal Sent'),
        ('follow_up', 'Follow Up'),
        ('negotiation', 'Negotiation'),
        ('contract', 'Contract Review'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True, related_name='sales_activities')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, null=True, blank=True, related_name='sales_activities')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='sales_activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    outcome = models.TextField(blank=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, help_text='Duration in minutes')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales_activities')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-scheduled_date', '-created_at']
        verbose_name_plural = 'Sales Activities'
    
    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.subject}"

class SalesPipeline(models.Model):
    """Sales pipeline configuration and management"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    stages = models.JSONField(default=list)  # Pipeline stages configuration
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class SalesForecast(models.Model):
    """Sales forecasting and projections"""
    FORECAST_PERIODS = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    period = models.CharField(max_length=20, choices=FORECAST_PERIODS)
    start_date = models.DateField()
    end_date = models.DateField()
    projected_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    actual_revenue = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    confidence_level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sales_forecasts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.get_period_display()} Forecast - {self.start_date} to {self.end_date}"
