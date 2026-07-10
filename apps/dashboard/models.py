from django.db import models
from django.conf import settings

class UserStat(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dashboard_stat')
    career_readiness = models.IntegerField(default=0)
    skills_strength = models.IntegerField(default=0)
    profile_progress = models.IntegerField(default=0)
    ai_score = models.IntegerField(default=0)
    day_streak = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Stats for {self.user.username}"

class RoadmapPhase(models.Model):
    STATUS_CHOICES = (
        ('Completed', 'Completed'),
        ('In Progress', 'In Progress'),
        ('Upcoming', 'Upcoming'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='roadmap_phases')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Upcoming')
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class AIInsight(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_insights')
    title = models.CharField(max_length=150)
    message = models.TextField()
    time_ago = models.CharField(max_length=50) # e.g. "2h ago", "1d ago"
    icon_type = models.CharField(max_length=50, default='trend') # 'trend', 'growth', 'streak'
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    @staticmethod
    def placeholder_titles():
        return [
            'Your communication skills are strong!',
            'Data Analysis is a high growth skill for you.',
            "You're consistent! 🔥",
        ]

    def is_sample(self):
        return self.title in self.placeholder_titles()

    def __str__(self):
        return self.title

class RecommendedOpportunity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='opportunities')
    title = models.CharField(max_length=150)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=50) # e.g., 'Internship', 'Virtual'
    time_left = models.CharField(max_length=50) # e.g., '2d left'
    logo_url = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']

    @staticmethod
    def sample_companies():
        return ['Microsoft', 'Google', 'SmartBridge']

    def is_sample(self):
        normalized_title = self.title.lower()
        return (
            self.company in self.sample_companies() and
            ('intern' in normalized_title or 'virtual' in normalized_title)
        )

    def __str__(self):
        return f"{self.title} at {self.company}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=150)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Achievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=50) # e.g. icon name
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-unlocked_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"
