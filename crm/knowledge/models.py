from django.db import models
from django.contrib.auth.models import User
from crm.core.models import Company, Customer


class KnowledgeCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='knowledge_categories')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Knowledge categories"
        unique_together = ['name', 'company']
    
    def __str__(self):
        return self.name


class KnowledgeArticle(models.Model):
    ARTICLE_STATUS = [
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    ARTICLE_TYPES = [
        ('how_to', 'How-To Guide'),
        ('troubleshooting', 'Troubleshooting'),
        ('faq', 'FAQ'),
        ('tutorial', 'Tutorial'),
        ('reference', 'Reference'),
        ('best_practice', 'Best Practice'),
        ('announcement', 'Announcement'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    summary = models.TextField(blank=True)
    category = models.ForeignKey(KnowledgeCategory, on_delete=models.CASCADE, related_name='articles')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='knowledge_articles')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_articles')
    status = models.CharField(max_length=20, choices=ARTICLE_STATUS, default='draft')
    article_type = models.CharField(max_length=20, choices=ARTICLE_TYPES, default='how_to')
    
    # SEO and visibility
    meta_description = models.TextField(blank=True)
    keywords = models.CharField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    
    # Tracking
    views_count = models.PositiveIntegerField(default=0)
    helpful_votes = models.PositiveIntegerField(default=0)
    not_helpful_votes = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_articles')
    
    # Related content
    related_articles = models.ManyToManyField('self', blank=True, symmetrical=False)
    tags = models.ManyToManyField('KnowledgeTag', blank=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        unique_together = ['slug', 'company']
    
    def __str__(self):
        return self.title
    
    def get_helpful_ratio(self):
        total_votes = self.helpful_votes + self.not_helpful_votes
        if total_votes == 0:
            return 0
        return (self.helpful_votes / total_votes) * 100


class KnowledgeTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='knowledge_tags')
    color = models.CharField(max_length=7, default='#3B82F6')  # Hex color code
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class KnowledgeComment(models.Model):
    article = models.ForeignKey(KnowledgeArticle, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='knowledge_comments')
    content = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_approved = models.BooleanField(default=True)
    helpful_votes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.article.title}"


class KnowledgeFeedback(models.Model):
    FEEDBACK_TYPES = [
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
        ('suggestion', 'Suggestion'),
        ('error', 'Error Report'),
        ('praise', 'Praise'),
    ]
    
    article = models.ForeignKey(KnowledgeArticle, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='knowledge_feedback')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    comment = models.TextField(blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True)  # 1-5 rating
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['article', 'user', 'feedback_type']
    
    def __str__(self):
        return f"{self.feedback_type} feedback on {self.article.title}"


class KnowledgeSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='knowledge_searches')
    query = models.CharField(max_length=500)
    results_count = models.PositiveIntegerField(default=0)
    clicked_article = models.ForeignKey(KnowledgeArticle, on_delete=models.SET_NULL, null=True, blank=True)
    search_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-search_time']
        verbose_name_plural = "Knowledge searches"
    
    def __str__(self):
        return f"'{self.query}' searched at {self.search_time}"


class KnowledgeTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content_template = models.TextField()
    category = models.ForeignKey(KnowledgeCategory, on_delete=models.CASCADE, related_name='templates')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='knowledge_templates')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class KnowledgeAnalytics(models.Model):
    article = models.ForeignKey(KnowledgeArticle, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()
    
    # Daily metrics
    views = models.PositiveIntegerField(default=0)
    unique_views = models.PositiveIntegerField(default=0)
    time_spent = models.DurationField(default=0)  # Total time spent reading
    shares = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)
    
    # Engagement metrics
    bounce_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Percentage of users who left without interaction
    scroll_depth = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Average scroll depth percentage
    
    class Meta:
        ordering = ['-date']
        unique_together = ['article', 'date']
        verbose_name_plural = "Knowledge analytics"
    
    def __str__(self):
        return f"{self.article.title} - {self.date}"


class KnowledgeVersion(models.Model):
    article = models.ForeignKey(KnowledgeArticle, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField(blank=True)
    changes_summary = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_versions')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-version_number']
        unique_together = ['article', 'version_number']
    
    def __str__(self):
        return f"{self.article.title} v{self.version_number}"
