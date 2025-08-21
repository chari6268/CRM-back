from django.db import models
from django.contrib.auth.models import User
from crm.core.models import Customer, Company


class Survey(models.Model):
    SURVEY_TYPES = [
        ('customer_satisfaction', 'Customer Satisfaction'),
        ('nps', 'Net Promoter Score'),
        ('product_feedback', 'Product Feedback'),
        ('support_quality', 'Support Quality'),
        ('onboarding', 'Onboarding Experience'),
        ('custom', 'Custom Survey'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    survey_type = models.CharField(max_length=50, choices=SURVEY_TYPES)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='surveys')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.company.name}"


class SurveyQuestion(models.Model):
    QUESTION_TYPES = [
        ('text', 'Text Input'),
        ('textarea', 'Long Text'),
        ('radio', 'Single Choice'),
        ('checkbox', 'Multiple Choice'),
        ('rating', 'Rating Scale'),
        ('nps', 'NPS Scale (0-10)'),
        ('likert', 'Likert Scale'),
        ('date', 'Date Picker'),
        ('email', 'Email Input'),
    ]
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    is_required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    options = models.JSONField(blank=True, null=True)  # For radio/checkbox questions
    min_value = models.IntegerField(null=True, blank=True)  # For rating scales
    max_value = models.IntegerField(null=True, blank=True)  # For rating scales
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.survey.title} - Q{self.order}: {self.question_text[:50]}"


class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='survey_responses')
    respondent_email = models.EmailField(blank=True)
    respondent_name = models.CharField(max_length=100, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-started_at']
        unique_together = ['survey', 'customer']
    
    def __str__(self):
        return f"{self.survey.title} - {self.customer.name}"


class SurveyAnswer(models.Model):
    response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True)
    answer_value = models.IntegerField(null=True, blank=True)  # For numeric answers
    answer_options = models.JSONField(blank=True, null=True)  # For multiple choice answers
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['response', 'question']
    
    def __str__(self):
        return f"{self.response} - {self.question.question_text[:50]}"


class NPSScore(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='nps_scores')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='nps_scores')
    score = models.IntegerField(choices=[(i, str(i)) for i in range(11)])  # 0-10 scale
    feedback = models.TextField(blank=True)
    survey_response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, related_name='nps_scores')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['customer', 'company', 'survey_response']
    
    def __str__(self):
        return f"NPS {self.score} - {self.customer.name}"


class SurveyTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    survey_type = models.CharField(max_length=50, choices=Survey.SURVEY_TYPES)
    questions = models.JSONField()  # Store question structure
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='survey_templates')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.survey_type}"


class SurveyMetrics(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='metrics')
    total_sent = models.PositiveIntegerField(default=0)
    total_responses = models.PositiveIntegerField(default=0)
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    average_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    nps_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    last_calculated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Survey metrics"
    
    def __str__(self):
        return f"{self.survey.title} - {self.completion_rate}% completion"
