from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from crm.core.models import Company, Customer
import uuid

class Contact(models.Model):
    """Enhanced contact management with social media and communication preferences"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    is_decision_maker = models.BooleanField(default=False)
    social_media = models.JSONField(default=dict, blank=True)  # LinkedIn, Twitter, etc.
    communication_preferences = models.JSONField(default=dict, blank=True)  # Email, SMS, Phone
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_primary', 'last_name', 'first_name']
        unique_together = ['customer', 'email']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.customer.name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class CustomerSegment(models.Model):
    """Customer segmentation for targeted marketing and analysis"""
    SEGMENT_CHOICES = [
        ('enterprise', 'Enterprise'),
        ('mid_market', 'Mid-Market'),
        ('small_business', 'Small Business'),
        ('startup', 'Startup'),
        ('individual', 'Individual'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    segment_type = models.CharField(max_length=20, choices=SEGMENT_CHOICES)
    description = models.TextField(blank=True)
    criteria = models.JSONField(default=dict)  # Segmentation criteria
    color = models.CharField(max_length=7, default='#3B82F6')  # Hex color
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class CustomerTag(models.Model):
    """Flexible tagging system for customers"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#6B7280')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class CustomerActivity(models.Model):
    """Track all customer activities and interactions"""
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('purchase', 'Purchase'),
        ('support', 'Support Request'),
        ('feedback', 'Feedback'),
        ('survey', 'Survey Response'),
        ('email', 'Email Interaction'),
        ('call', 'Phone Call'),
        ('meeting', 'Meeting'),
        ('demo', 'Product Demo'),
        ('trial', 'Trial Usage'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)  # Additional activity data
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Customer Activities'
    
    def __str__(self):
        return f"{self.customer.name} - {self.get_activity_type_display()}"

class CustomerPreference(models.Model):
    """Store customer preferences and settings"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='preferences')
    language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='UTC')
    currency = models.CharField(max_length=3, default='USD')
    notification_settings = models.JSONField(default=dict)
    ui_preferences = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Preferences for {self.customer.name}"

class CustomerDocument(models.Model):
    """Store customer-related documents and files"""
    DOCUMENT_TYPES = [
        ('contract', 'Contract'),
        ('invoice', 'Invoice'),
        ('proposal', 'Proposal'),
        ('case_study', 'Case Study'),
        ('nda', 'NDA'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='customer_documents/')
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(CustomerTag, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.title} - {self.customer.name}"
