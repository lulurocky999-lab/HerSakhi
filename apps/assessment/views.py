import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import AssessmentResponse
from apps.accounts.models import UserProfile
from ai.services import extract_career_insights
from apps.dashboard.models import UserStat, Achievement

@csrf_exempt
@login_required
def submit_assessment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create AssessmentResponse
            assessment = AssessmentResponse.objects.create(
                user=request.user,
                raw_data=data
            )
            
            # Update User Profile
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            
            # Map JSON to profile based on the 8 sections
            profile.education_level = data.get('education_level', '')
            profile.degree = data.get('degree', '')
            profile.graduation_year = data.get('graduation_year', '')
            profile.current_status = data.get('current_status', '')
            
            profile.interests = data.get('interests', [])
            profile.technical_skills = data.get('technical_skills', [])
            profile.soft_skills = data.get('soft_skills', [])
            
            profile.dream_role = data.get('dream_role', '')
            profile.dream_company = data.get('dream_company', '')
            profile.expected_salary = data.get('expected_salary', '')
            profile.preferred_industry = data.get('preferred_industry', '')
            profile.preferred_work_type = data.get('preferred_work_type', '')
            
            profile.learning_style = data.get('learning_style', [])
            
            profile.work_style = data.get('work_style', '')
            profile.decision_making = data.get('decision_making', '')
            profile.team_preference = data.get('team_preference', '')
            profile.leadership_preference = data.get('leadership_preference', '')
            
            profile.career_obstacles = data.get('career_obstacles', '')
            profile.confidence_level = data.get('confidence_level', '')
            profile.areas_for_improvement = data.get('areas_for_improvement', '')
            
            profile.is_onboarded = True
            profile.save()
            
            # Call AI Service for Insights
            insights = extract_career_insights(data)
            
            if insights.get('success') is not False:
                assessment.ai_insights = insights
                assessment.save()
                
                # Update Dashboard Stats
                stat, _ = UserStat.objects.get_or_create(user=request.user)
                stat.career_readiness = insights.get('career_readiness_score', stat.career_readiness)
                if stat.profile_progress < 100:
                    stat.profile_progress = min(100, stat.profile_progress + 50)
                stat.save()
            
            # Unlock Achievement
            Achievement.objects.get_or_create(
                user=request.user,
                title="Assessment Completed",
                defaults={
                    "description": "Completed the 8-section career assessment.",
                    "icon": "check-circle"
                }
            )

            return JsonResponse({
                'success': True,
                'insights': insights
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
            
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def index(request):
    return render(request, 'assessment/index.html')
