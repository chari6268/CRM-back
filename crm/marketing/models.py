from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from crm.core.models import Customer, Company
import uuid

class MarketingCampaign(models.Model):
    """Marketing campaign management"""
    CAMPAIGN_TYPES = [
        ('email', 'Email Campaign'),
        ('social_media', 'Social Media'),
        ('content', 'Content Marketing'),
        ('advertising', 'Digital Advertising'),
        ('event', 'Event Marketing'),
        ('referral', 'Referral Program'),
        ('other', 'Other'),
    ]
    
    CAMPAIGN_STATUS = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    campaign_type = models.CharField(max_length=20, choices=CAMPAIGN_TYPES)
    status = models.CharField(max_length=20, choices=CAMPAIGN_STATUS, default='draft')
    description = models.TextField(blank=True)
    target_audience = models.JSONField(default=dict)  # Target criteria
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    goals = models.JSONField(default=list)  # Campaign goals
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_campaigns')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_campaigns')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_campaign_type_display()}"

class EmailCampaign(models.Model):
    """Email marketing campaigns with templates and automation"""
    EMAIL_TYPES = [
        ('newsletter', 'Newsletter'),
        ('promotional', 'Promotional'),
        ('onboarding', 'Onboarding'),
        ('abandoned_cart', 'Abandoned Cart'),
        ('birthday', 'Birthday'),
        ('anniversary', 'Anniversary'),
        ('re_engagement', 'Re-engagement'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(MarketingCampaign, on_delete=models.CASCADE, related_name='email_campaigns')
    name = models.CharField(max_length=200)
    email_type = models.CharField(max_length=20, choices=EMAIL_TYPES)
    subject_line = models.CharField(max_length=200)
    preheader = models.CharField(max_length=200, blank=True)
    html_content = models.TextField()
    text_content = models.TextField(blank=True)
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    reply_to_email = models.EmailField(blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_email_campaigns')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_at', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject_line}"

class EmailTemplate(models.Model):
    """Reusable email templates"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject_line = models.CharField(max_length=200)
    html_content = models.TextField()
    text_content = models.TextField(blank=True)
    variables = models.JSONField(default=list)  # Template variables
    category = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_email_templates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class EmailSubscriber(models.Model):
    """Email list subscribers with preferences and tracking"""
    SUBSCRIPTION_STATUS = [
        ('subscribed', 'Subscribed'),
        ('unsubscribed', 'Unsubscribed'),
        ('pending', 'Pending'),
        ('bounced', 'Bounced'),
        ('spam', 'Marked as Spam'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUS, default='subscribed')
    source = models.CharField(max_length=100, blank=True)  # How they subscribed
    preferences = models.JSONField(default=dict)  # Email preferences
    tags = models.JSONField(default=list)  # Subscriber tags
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    last_email_sent = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

class EmailSend(models.Model):
    """Track individual email sends and performance"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_campaign = models.ForeignKey(EmailCampaign, on_delete=models.CASCADE, related_name='email_sends')
    subscriber = models.ForeignKey(EmailSubscriber, on_delete=models.CASCADE, related_name='email_sends')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='email_sends')
    sent_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    bounced = models.BooleanField(default=False)
    bounce_reason = models.TextField(blank=True)
    unsubscribed = models.BooleanField(default=False)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-sent_at']
        unique_together = ['email_campaign', 'subscriber']
    
    def __str__(self):
        return f"{self.email_campaign.name} to {self.subscriber.email}"

class SocialMediaCampaign(models.Model):
    """Social media marketing campaigns"""
    PLATFORMS = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(MarketingCampaign, on_delete=models.CASCADE, related_name='social_campaigns')
    platform = models.CharField(max_length=20, choices=PLATFORMS)
    content = models.TextField()
    media_files = models.JSONField(default=list)  # Media file URLs
    scheduled_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    post_url = models.URLField(blank=True)
    engagement_metrics = models.JSONField(default=dict)  # Likes, shares, comments, etc.
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_social_campaigns')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-scheduled_at', '-created_at']
    
    def __str__(self):
        return f"{self.campaign.name} - {self.get_platform_display()}"

class MarketingAutomation(models.Model):
    """Marketing automation workflows and triggers"""
    TRIGGER_TYPES = [
        ('user_action', 'User Action'),
        ('time_based', 'Time Based'),
        ('email_engagement', 'Email Engagement'),
        ('purchase', 'Purchase'),
        ('website_visit', 'Website Visit'),
        ('form_submission', 'Form Submission'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    trigger_type = models.CharField(max_length=20, choices=TRIGGER_TYPES)
    trigger_conditions = models.JSONField(default=dict)  # Trigger conditions
    actions = models.JSONField(default=list)  # Automation actions
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_automations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class MarketingMetrics(models.Model):
    """Marketing performance metrics and KPIs"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(MarketingCampaign, on_delete=models.CASCADE, related_name='metrics')
    date = models.DateField()
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    roi = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    ctr = models.DecimalField(max_digits=8, decimal_places=4, default=0)  # Click-through rate
    cpc = models.DecimalField(max_digits=8, decimal_places=4, default=0)  # Cost per click
    cpa = models.DecimalField(max_digits=8, decimal_places=4, default=0)  # Cost per acquisition
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['campaign', 'date']
    
    def __str__(self):
        return f"{self.campaign.name} - {self.date}"
