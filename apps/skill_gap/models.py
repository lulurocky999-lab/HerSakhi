from django.db import models
from django.conf import settings

class SkillGapAnalysis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='skill_gaps')
    target_role = models.CharField(max_length=150)
    
    # AI JSON result containing current_skills, missing_skills, recommendations
    analysis_data = models.JSONField(default=dict)
    
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"Skill Gap for {self.user.username} -> {self.target_role}"
