from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.dashboard.models import Achievement, UserStat

@login_required
def index(request):
    achievements = request.user.achievements.order_by('-unlocked_at')
    total_achievements = achievements.count()
    recent_achievements = achievements[:4]
    badges = achievements[:5]
    progress_percent = int(min(100, (total_achievements / 25) * 100)) if total_achievements else 0
    milestone_progress = min(total_achievements, 25)
    remaining_for_milestone = max(0, 25 - total_achievements)
    next_milestone_title = 'Master Achiever' if total_achievements >= 25 else 'Expert Learner'
    next_milestone_description = (
        'You have unlocked the main milestone. Keep going!' if total_achievements >= 25
        else f'Complete {remaining_for_milestone} more achievements to unlock this milestone'
    )

    stat, _ = UserStat.objects.get_or_create(user=request.user)
    profile = getattr(request.user, 'profile', None)
    skills_mastered = len(profile.technical_skills) if profile and profile.technical_skills else 0
    day_streak = stat.day_streak
    career_readiness = stat.career_readiness
    profile_progress = stat.profile_progress

    categories = []
    if total_achievements:
        category_counts = {}
        for achievement in achievements:
            category_name = achievement.icon.title() if achievement.icon else 'General'
            category_counts[category_name] = category_counts.get(category_name, 0) + 1

        colors = ['green', 'blue', 'orange', 'purple']
        for index, (name, count) in enumerate(category_counts.items()):
            categories.append({
                'name': name,
                'count': count,
                'percentage': int(min(100, (count / total_achievements) * 100)),
                'color': colors[index % len(colors)]
            })

    return render(request, 'achievements/index.html', {
        'achievements': achievements,
        'total_achievements': total_achievements,
        'recent_achievements': recent_achievements,
        'badges': badges,
        'progress_percent': progress_percent,
        'milestone_progress': milestone_progress,
        'next_milestone_title': next_milestone_title,
        'next_milestone_description': next_milestone_description,
        'categories': categories,
        'day_streak': day_streak,
        'skills_mastered': skills_mastered,
        'career_readiness': career_readiness,
        'profile_progress': profile_progress,
    })
