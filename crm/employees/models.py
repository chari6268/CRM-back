from django.db import models
from django.contrib.auth.models import User
from crm.core.models import Company, Customer


class Employee(models.Model):
    EMPLOYEE_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('terminated', 'Terminated'),
        ('on_leave', 'On Leave'),
    ]
    
    EMPLOYEE_ROLES = [
        ('sales_rep', 'Sales Representative'),
        ('sales_manager', 'Sales Manager'),
        ('support_agent', 'Support Agent'),
        ('support_manager', 'Support Manager'),
        ('marketing_specialist', 'Marketing Specialist'),
        ('marketing_manager', 'Marketing Manager'),
        ('admin', 'Administrator'),
        ('analyst', 'Data Analyst'),
        ('manager', 'Manager'),
        ('executive', 'Executive'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
    employee_id = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=30, choices=EMPLOYEE_ROLES)
    department = models.CharField(max_length=100)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    hire_date = models.DateField()
    status = models.CharField(max_length=20, choices=EMPLOYEE_STATUS, default='active')
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['user__last_name', 'user__first_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"


class EmployeePerformance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_records')
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Sales Performance
    sales_target = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sales_achieved = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    sales_conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Support Performance
    tickets_handled = models.PositiveIntegerField(default=0)
    tickets_resolved = models.PositiveIntegerField(default=0)
    average_resolution_time = models.DurationField(null=True, blank=True)
    customer_satisfaction_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    
    # Marketing Performance
    campaigns_managed = models.PositiveIntegerField(default=0)
    leads_generated = models.PositiveIntegerField(default=0)
    email_open_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    email_click_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Overall Performance
    productivity_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    quality_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    overall_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    
    notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews_given')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-period_end']
        unique_together = ['employee', 'period_start', 'period_end']
    
    def __str__(self):
        return f"{self.employee} - {self.period_start} to {self.period_end}"


class EmployeeActivity(models.Model):
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('customer_interaction', 'Customer Interaction'),
        ('ticket_created', 'Support Ticket Created'),
        ('ticket_resolved', 'Support Ticket Resolved'),
        ('lead_created', 'Lead Created'),
        ('deal_closed', 'Deal Closed'),
        ('email_sent', 'Email Sent'),
        ('call_made', 'Call Made'),
        ('meeting_attended', 'Meeting Attended'),
        ('training_completed', 'Training Completed'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPES)
    description = models.TextField()
    related_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    related_company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    metadata = models.JSONField(blank=True, null=True)  # Additional activity data
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True, blank=True)  # For activities with duration
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Employee activities"
    
    def __str__(self):
        return f"{self.employee} - {self.activity_type} at {self.timestamp}"


class EmployeeGoal(models.Model):
    GOAL_TYPES = [
        ('sales', 'Sales Target'),
        ('support', 'Support Target'),
        ('marketing', 'Marketing Target'),
        ('productivity', 'Productivity Target'),
        ('quality', 'Quality Target'),
        ('training', 'Training Target'),
        ('personal', 'Personal Development'),
    ]
    
    GOAL_STATUS = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('on_track', 'On Track'),
        ('at_risk', 'At Risk'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    target_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    target_date = models.DateField()
    start_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=GOAL_STATUS, default='not_started')
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    manager_notes = models.TextField(blank=True)
    employee_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['target_date']
    
    def __str__(self):
        return f"{self.employee} - {self.title}"


class EmployeeTraining(models.Model):
    TRAINING_TYPES = [
        ('product', 'Product Training'),
        ('sales', 'Sales Training'),
        ('support', 'Support Training'),
        ('marketing', 'Marketing Training'),
        ('compliance', 'Compliance Training'),
        ('soft_skills', 'Soft Skills'),
        ('technical', 'Technical Skills'),
        ('leadership', 'Leadership Development'),
    ]
    
    TRAINING_STATUS = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('expired', 'Expired'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='trainings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    training_type = models.CharField(max_length=20, choices=TRAINING_TYPES)
    provider = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=TRAINING_STATUS, default='not_started')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    certificate_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.employee} - {self.title}"


class EmployeeSchedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_start = models.TimeField(null=True, blank=True)
    break_end = models.TimeField(null=True, blank=True)
    is_working_day = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['employee', 'date']
    
    def __str__(self):
        return f"{self.employee} - {self.date} ({self.start_time}-{self.end_time})"


class EmployeeMetrics(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='metrics')
    date = models.DateField()
    
    # Daily metrics
    hours_worked = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    tasks_completed = models.PositiveIntegerField(default=0)
    customer_interactions = models.PositiveIntegerField(default=0)
    tickets_handled = models.PositiveIntegerField(default=0)
    sales_activities = models.PositiveIntegerField(default=0)
    
    # Performance indicators
    efficiency_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    quality_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['employee', 'date']
        verbose_name_plural = "Employee metrics"
    
    def __str__(self):
        return f"{self.employee} - {self.date}"
