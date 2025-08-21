from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from crm.core.models import Customer, Company
import uuid

class AIModel(models.Model):
    """AI model definitions and configurations"""
    MODEL_TYPES = [
        ('churn_prediction', 'Churn Prediction'),
        ('lead_scoring', 'Lead Scoring'),
        ('customer_segmentation', 'Customer Segmentation'),
        ('sentiment_analysis', 'Sentiment Analysis'),
        ('recommendation_engine', 'Recommendation Engine'),
        ('anomaly_detection', 'Anomaly Detection'),
        ('forecasting', 'Forecasting'),
        ('classification', 'Classification'),
        ('regression', 'Regression'),
        ('custom', 'Custom Model'),
    ]
    
    STATUS_CHOICES = [
        ('training', 'Training'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('deprecated', 'Deprecated'),
        ('error', 'Error'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    model_type = models.CharField(max_length=30, choices=MODEL_TYPES)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=20, default='1.0.0')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='training')
    model_file_path = models.CharField(max_length=500, blank=True)
    model_config = models.JSONField(default=dict)  # Model configuration
    hyperparameters = models.JSONField(default=dict)  # Model hyperparameters
    training_data_info = models.JSONField(default=dict)  # Training data information
    performance_metrics = models.JSONField(default=dict)  # Model performance metrics
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_ai_models')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_trained = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['name', 'version']
    
    def __str__(self):
        return f"{self.name} v{self.version} - {self.get_model_type_display()}"

class PredictiveScore(models.Model):
    """Predictive scoring for various business metrics"""
    SCORE_TYPES = [
        ('churn_risk', 'Churn Risk'),
        ('lead_score', 'Lead Score'),
        ('customer_lifetime_value', 'Customer Lifetime Value'),
        ('purchase_probability', 'Purchase Probability'),
        ('upsell_probability', 'Upsell Probability'),
        ('support_priority', 'Support Priority'),
        ('fraud_risk', 'Fraud Risk'),
        ('custom', 'Custom Score'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='predictive_scores')
    score_type = models.CharField(max_length=30, choices=SCORE_TYPES)
    score_value = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    confidence_level = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    factors = models.JSONField(default=list)  # Factors contributing to the score
    ai_model = models.ForeignKey(AIModel, on_delete=models.SET_NULL, null=True, related_name='predictions')
    calculated_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-calculated_at']
        unique_together = ['customer', 'score_type']
    
    def __str__(self):
        return f"{self.customer.name} - {self.get_score_type_display()}: {self.score_value}"

class Chatbot(models.Model):
    """AI chatbot configurations and conversations"""
    BOT_TYPES = [
        ('customer_support', 'Customer Support'),
        ('lead_qualification', 'Lead Qualification'),
        ('sales_assistant', 'Sales Assistant'),
        ('onboarding', 'Onboarding'),
        ('faq', 'FAQ Bot'),
        ('custom', 'Custom Bot'),
    ]
    
    PLATFORMS = [
        ('website', 'Website'),
        ('mobile_app', 'Mobile App'),
        ('messenger', 'Facebook Messenger'),
        ('whatsapp', 'WhatsApp'),
        ('slack', 'Slack'),
        ('teams', 'Microsoft Teams'),
        ('api', 'API'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    bot_type = models.CharField(max_length=30, choices=BOT_TYPES)
    platform = models.CharField(max_length=20, choices=PLATFORMS)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    configuration = models.JSONField(default=dict)  # Bot configuration
    training_data = models.JSONField(default=list)  # Training data and responses
    ai_model = models.ForeignKey(AIModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='chatbots')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_chatbots')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_bot_type_display()}"

class ChatbotConversation(models.Model):
    """Individual chatbot conversations"""
    CONVERSATION_STATUS = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('escalated', 'Escalated to Human'),
        ('abandoned', 'Abandoned'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE, related_name='conversations')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='chatbot_conversations')
    session_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=CONVERSATION_STATUS, default='active')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    metadata = models.JSONField(default=dict)  # Additional conversation metadata
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.chatbot.name} - {self.session_id}"

class ChatbotMessage(models.Model):
    """Individual messages in chatbot conversations"""
    MESSAGE_TYPES = [
        ('user', 'User Message'),
        ('bot', 'Bot Response'),
        ('system', 'System Message'),
        ('escalation', 'Escalation Message'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(ChatbotConversation, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    intent_detected = models.CharField(max_length=100, blank=True)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    entities = models.JSONField(default=list)  # Named entities extracted
    metadata = models.JSONField(default=dict)  # Additional message metadata
    
    class Meta:
        ordering = ['conversation', 'timestamp']
    
    def __str__(self):
        return f"{self.conversation.session_id} - {self.get_message_type_display()} at {self.timestamp}"

class PersonalizationRule(models.Model):
    """Personalization rules and targeting"""
    RULE_TYPES = [
        ('content', 'Content Personalization'),
        ('product', 'Product Recommendation'),
        ('pricing', 'Pricing Personalization'),
        ('communication', 'Communication Personalization'),
        ('ui_ux', 'UI/UX Personalization'),
        ('workflow', 'Workflow Personalization'),
        ('custom', 'Custom Personalization'),
    ]
    
    TRIGGER_TYPES = [
        ('user_action', 'User Action'),
        ('time_based', 'Time Based'),
        ('location_based', 'Location Based'),
        ('behavior_based', 'Behavior Based'),
        ('segment_based', 'Segment Based'),
        ('ai_prediction', 'AI Prediction'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    rule_type = models.CharField(max_length=30, choices=RULE_TYPES)
    trigger_type = models.CharField(max_length=20, choices=TRIGGER_TYPES)
    description = models.TextField(blank=True)
    trigger_conditions = models.JSONField(default=dict)  # Trigger conditions
    personalization_logic = models.JSONField(default=dict)  # Personalization logic
    target_audience = models.JSONField(default=dict)  # Target audience criteria
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_personalization_rules')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['priority', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_rule_type_display()}"

class AIRecommendation(models.Model):
    """AI-powered recommendations for customers"""
    RECOMMENDATION_TYPES = [
        ('product', 'Product Recommendation'),
        ('content', 'Content Recommendation'),
        ('offer', 'Offer Recommendation'),
        ('action', 'Action Recommendation'),
        ('upsell', 'Upsell Recommendation'),
        ('cross_sell', 'Cross-sell Recommendation'),
        ('retention', 'Retention Recommendation'),
        ('custom', 'Custom Recommendation'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='ai_recommendations')
    recommendation_type = models.CharField(max_length=30, choices=RECOMMENDATION_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    recommendation_data = models.JSONField(default=dict)  # Recommendation details
    confidence_score = models.DecimalField(max_digits=5, decimal_places=4, validators=[MinValueValidator(0), MaxValueValidator(1)])
    ai_model = models.ForeignKey(AIModel, on_delete=models.SET_NULL, null=True, related_name='recommendations')
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(null=True, blank=True)
    is_acted_upon = models.BooleanField(default=False)
    acted_upon_at = models.DateTimeField(null=True, blank=True)
    feedback_score = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-confidence_score', '-created_at']
    
    def __str__(self):
        return f"{self.customer.name} - {self.get_recommendation_type_display()}: {self.title}"

class AITrainingData(models.Model):
    """Training data for AI models"""
    DATA_TYPES = [
        ('conversation', 'Conversation Data'),
        ('behavior', 'Behavior Data'),
        ('feedback', 'Feedback Data'),
        ('transaction', 'Transaction Data'),
        ('interaction', 'Interaction Data'),
        ('custom', 'Custom Data'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_type = models.CharField(max_length=20, choices=DATA_TYPES)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    data_content = models.JSONField(default=dict)  # Training data content
    metadata = models.JSONField(default=dict)  # Data metadata
    quality_score = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_training_data')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_training_data')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_data_type_display()}"

class AIModelPerformance(models.Model):
    """AI model performance tracking"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ai_model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='performance_records')
    date = models.DateField()
    total_predictions = models.IntegerField(default=0)
    accurate_predictions = models.IntegerField(default=0)
    accuracy_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    precision = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    recall = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    f1_score = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    avg_response_time = models.DecimalField(max_digits=8, decimal_places=4, default=0)  # In seconds
    error_count = models.IntegerField(default=0)
    error_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['ai_model', 'date']
    
    def __str__(self):
        return f"{self.ai_model.name} Performance - {self.date}"
