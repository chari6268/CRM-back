from django.db import models
from django.contrib.auth import get_user_model
from crm.core.models import Customer, Company
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class ChurnRisk(models.Model):
    """Model for tracking customer churn risk."""
    RISK_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='churn_risks')
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    risk_score = models.DecimalField(max_digits=5, decimal_places=2)
    factors = models.JSONField(default=dict)
    last_calculated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'crm_churn_risks'
        ordering = ['-risk_score']

    def __str__(self):
        return f"{self.customer.full_name} - {self.risk_level} Risk ({self.risk_score})"


class CustomerMetrics(models.Model):
    """Model for tracking customer engagement metrics."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='metrics')
    date = models.DateField()
    login_frequency = models.IntegerField(default=0)
    feature_usage = models.JSONField(default=dict)
    support_tickets = models.IntegerField(default=0)
    satisfaction_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'crm_customer_metrics'
        unique_together = ['customer', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.customer.full_name} - {self.date}"


class SentimentAnalysis(models.Model):
    """Model for tracking customer sentiment."""
    SENTIMENT_TYPES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sentiments')
    source = models.CharField(max_length=100)  # email, survey, support, social
    sentiment = models.CharField(max_length=20, choices=SENTIMENT_TYPES)
    confidence_score = models.DecimalField(max_digits=3, decimal_places=2)
    text_content = models.TextField()
    keywords = models.JSONField(default=list)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'crm_sentiment_analysis'
        ordering = ['-date']

    def __str__(self):
        return f"{self.customer.full_name} - {self.sentiment} ({self.source})"


class ProductFeedback(models.Model):
    """Model for tracking product feedback."""
    FEEDBACK_TYPES = [
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
        ('improvement', 'Improvement'),
        ('compliment', 'Compliment'),
        ('complaint', 'Complaint'),
    ]

    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='product_feedback')
    type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')
    title = models.CharField(max_length=200)
    description = models.TextField()
    rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    status = models.CharField(max_length=20, default='open')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'crm_product_feedback'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.customer.full_name}"
