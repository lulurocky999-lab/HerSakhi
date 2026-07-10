from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom user model for HerSakhi."""
    dream_career = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Section 1 - Personal Background
    education_level = models.CharField(max_length=100, blank=True)
    degree = models.CharField(max_length=100, blank=True)
    graduation_year = models.CharField(max_length=100, blank=True)
    current_status = models.CharField(max_length=100, blank=True)
    
    # Section 2 - Interests (stored as JSON array of strings)
    interests = models.JSONField(default=list, blank=True)
    
    # Section 3 - Technical Skills (stored as JSON array of objects: {skill: str, proficiency: str})
    technical_skills = models.JSONField(default=list, blank=True)
    
    # Section 4 - Soft Skills (stored as JSON array of strings)
    soft_skills = models.JSONField(default=list, blank=True)
    
    # Section 5 - Career Goals
    dream_role = models.CharField(max_length=100, blank=True)
    dream_company = models.CharField(max_length=100, blank=True)
    expected_salary = models.CharField(max_length=100, blank=True)
    preferred_industry = models.CharField(max_length=100, blank=True)
    preferred_work_type = models.CharField(max_length=100, blank=True)
    
    # Section 6 - Learning Style (stored as JSON array of strings)
    learning_style = models.JSONField(default=list, blank=True)
    
    # Section 7 - Personality
    work_style = models.CharField(max_length=100, blank=True)
    decision_making = models.CharField(max_length=100, blank=True)
    team_preference = models.CharField(max_length=100, blank=True)
    leadership_preference = models.CharField(max_length=100, blank=True)
    
    # Section 8 - Challenges
    career_obstacles = models.TextField(blank=True)
    confidence_level = models.CharField(max_length=50, blank=True)
    areas_for_improvement = models.TextField(blank=True)
    
    # Other context
    resume_text = models.TextField(blank=True)
    is_onboarded = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile for {self.user.username}"
