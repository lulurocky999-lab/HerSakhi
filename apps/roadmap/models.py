from django.db import models
from django.conf import settings

class CareerRoadmap(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='roadmaps')
    title = models.CharField(max_length=200)
    target_role = models.CharField(max_length=150)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    # Progress tracking
    completion_percentage = models.IntegerField(default=0)
    estimated_finish = models.CharField(max_length=100, blank=True)
    current_phase = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Roadmap for {self.user.username}: {self.title}"

class RoadmapMilestone(models.Model):
    roadmap = models.ForeignKey(CareerRoadmap, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.roadmap.user.username} - {self.title}"
