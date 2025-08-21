from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class User(AbstractUser):
    """Extended user model for CRM system."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'crm_users'

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    # Custom related_names to avoid conflicts with built-in User model
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='crm_user_set',
        related_query_name='crm_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='crm_user_set',
        related_query_name='crm_user',
    )


class Company(models.Model):
    """Company/Organization model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'crm_companies'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class Customer(models.Model):
    """Customer model."""
    CUSTOMER_STATUS = [
        ('lead', 'Lead'),
        ('prospect', 'Prospect'),
        ('customer', 'Customer'),
        ('churned', 'Churned'),
        ('inactive', 'Inactive'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='customers')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    position = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=CUSTOMER_STATUS, default='lead')
    source = models.CharField(max_length=100, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_customers')
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'crm_customers'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.company.name})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Interaction(models.Model):
    """Customer interaction model."""
    INTERACTION_TYPES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
        ('task', 'Task'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interactions')
    type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    duration = models.IntegerField(help_text='Duration in minutes', blank=True, null=True)
    outcome = models.TextField(blank=True)
    next_action = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'crm_interactions'
        ordering = ['-date']

    def __str__(self):
        return f"{self.type.title()} with {self.customer.full_name} on {self.date.strftime('%Y-%m-%d')}"


class Task(models.Model):
    """Task model for CRM activities."""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tasks', blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'crm_tasks'
        ordering = ['-due_date']

    def __str__(self):
        return f"{self.title} - {self.assigned_to.get_full_name()}"


class Notification(models.Model):
    """Notification model for system alerts."""
    NOTIFICATION_TYPES = [
        ('task_due', 'Task Due'),
        ('customer_update', 'Customer Update'),
        ('system_alert', 'System Alert'),
        ('reminder', 'Reminder'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    related_url = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'crm_notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} for {self.user.username}"
