from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.accounts.models import UserProfile
from apps.dashboard.models import UserStat

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile_and_stats(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        UserStat.objects.create(
            user=instance,
            career_readiness=0,
            skills_strength=0,
            profile_progress=0,
            ai_score=0,
            day_streak=0
        )

@receiver(post_save, sender=User)
def save_user_profile_and_stats(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
    
    try:
        instance.dashboard_stat.save()
    except UserStat.DoesNotExist:
        UserStat.objects.create(
            user=instance,
            career_readiness=0,
            skills_strength=0,
            profile_progress=0,
            ai_score=0,
            day_streak=0
        )
