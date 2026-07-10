from django.db import models
from django.conf import settings

class AssessmentResponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assessments')
    
    # Store the entire structured assessment as JSON
    raw_data = models.JSONField(default=dict)
    
    # Store the AI-generated insights/reports from this specific assessment
    ai_insights = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Assessment for {self.user.username} at {self.created_at}"
