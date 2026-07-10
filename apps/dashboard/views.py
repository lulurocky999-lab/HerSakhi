from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import UserStat, AIInsight, Notification, Achievement, RecommendedOpportunity
from apps.opportunities.models import Opportunity
from apps.roadmap.models import CareerRoadmap
from apps.assessment.models import AssessmentResponse
from apps.resume_lab.models import Resume

def update_user_stats(user):
    stat, _ = UserStat.objects.get_or_create(user=user)
    
    # 1. Profile Progress
    profile_progress = 0
    if hasattr(user, 'profile'):
        profile = user.profile
        if profile.dream_role:
            profile_progress += 20
        if profile.technical_skills:
            profile_progress += 20
        if profile.resume_text:
            profile_progress += 20

    # Assessment check
    if AssessmentResponse.objects.filter(user=user).exists():
        profile_progress += 30
        
    stat.profile_progress = min(profile_progress, 100)
    
    # 2. Skills Strength
    skills_strength = 0
    if hasattr(user, 'profile'):
        profile = user.profile
        skills_strength += min(len(profile.technical_skills) * 5, 60)
        skills_strength += min(len(profile.soft_skills) * 5, 20)
    stat.skills_strength = min(skills_strength, 100)
    
    # 3. AI Score
    latest_resume = Resume.objects.filter(user=user).first()
    ai_score = latest_resume.ats_score if latest_resume else 0
    
    # 4. Career Readiness
    roadmap = CareerRoadmap.objects.filter(user=user).first()
    roadmap_completion = roadmap.completion_percentage if roadmap else 0
    stat.career_readiness = int((stat.profile_progress + stat.skills_strength + roadmap_completion) / 3)
    
    stat.save()
    return stat

@login_required
def index_view(request):
    """Render the main dashboard."""
    stat = update_user_stats(request.user)
    profile = getattr(request.user, 'profile', None)

    # Get active roadmap if exists
    roadmap = CareerRoadmap.objects.filter(user=request.user).first()
    roadmap_phases = []
    roadmap_completion = roadmap.completion_percentage if roadmap else 0
    if roadmap:
        milestones = list(roadmap.milestones.all())
        first_uncompleted_index = next((i for i, m in enumerate(milestones) if not m.is_completed), len(milestones))
        for idx, milestone in enumerate(milestones):
            if milestone.is_completed:
                status = 'Completed'
            elif idx == first_uncompleted_index:
                status = 'In Progress'
            else:
                status = 'Upcoming'
            roadmap_phases.append({
                'title': milestone.title,
                'description': milestone.description,
                'status': status,
            })

    latest_resume = Resume.objects.filter(user=request.user).first()
    tech_count = len(profile.technical_skills) if profile and profile.technical_skills else 0
    soft_count = len(profile.soft_skills) if profile and profile.soft_skills else 0

    if not profile or not profile.dream_role:
        mission_title = "Define your dream role"
        mission_text = "Add your career goals so recommendations can personalize your journey."
        mission_progress = stat.profile_progress
        mission_url = reverse('accounts:profile')
    elif not latest_resume:
        mission_title = "Build your resume"
        mission_text = "Upload a resume to get AI feedback and improve your score."
        mission_progress = min(stat.profile_progress, 50)
        mission_url = reverse('resume_lab:index')
    elif not roadmap:
        mission_title = "Generate your roadmap"
        mission_text = "Create a step-by-step career plan based on your profile and skills."
        mission_progress = stat.career_readiness
        mission_url = reverse('roadmap:index')
    elif roadmap.completion_percentage < 100:
        mission_title = "Advance your career roadmap"
        mission_text = roadmap.current_phase or "Complete your next roadmap milestone."
        mission_progress = roadmap.completion_percentage
        mission_url = reverse('roadmap:index')
    else:
        mission_title = "Keep momentum"
        mission_text = "Continue exploring career opportunities and AI insights."
        mission_progress = min(stat.profile_progress, 100)
        mission_url = reverse('opportunities:index')

    ai_insights = [insight for insight in request.user.ai_insights.all() if not insight.is_sample()]
    opportunities = [opp for opp in RecommendedOpportunity.objects.filter(user=request.user) if not opp.is_sample()]

    context = {
        'stats': stat,
        'roadmap': roadmap,
        'roadmap_phases': roadmap_phases,
        'roadmap_completion': roadmap_completion,
        'ai_insights': ai_insights[:3],
        'opportunities': opportunities[:3],
        'recent_achievements': request.user.achievements.all()[:3],
        'notifications': request.user.notifications.all()[:5],
        'profile': profile,
        'latest_resume': latest_resume,
        'tech_count': tech_count,
        'soft_count': soft_count,
        'mission_title': mission_title,
        'mission_text': mission_text,
        'mission_progress': mission_progress,
        'mission_url': mission_url,
    }

    return render(request, 'dashboard/index.html', context)

@login_required
def get_notifications(request):
    notifications = request.user.notifications.all().order_by('-created_at')[:10]
    data = [{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'is_read': n.is_read,
        'time_ago': n.created_at.strftime('%Y-%m-%d %H:%M')
    } for n in notifications]
    return JsonResponse({'success': True, 'notifications': data})

@login_required
def mark_notification_read(request, notification_id):
    try:
        n = Notification.objects.get(id=notification_id, user=request.user)
        n.is_read = True
        n.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Not found'})

@login_required
def global_search(request):
    query = request.GET.get('q', '').lower()
    if not query:
        return JsonResponse({'success': True, 'results': []})
        
    results = []
    
    # Search Opportunities
    opps = Opportunity.objects.filter(title__icontains=query) | Opportunity.objects.filter(company__icontains=query)
    for opp in opps[:3]:
        results.append({'type': 'Opportunity', 'title': opp.title, 'desc': opp.company, 'url': '/opportunities/'})
        
    # Search Achievements
    achievements = request.user.achievements.filter(title__icontains=query)
    for a in achievements[:3]:
        results.append({'type': 'Achievement', 'title': a.title, 'desc': a.description, 'url': '/dashboard/'})
        
    return JsonResponse({'success': True, 'results': results})
