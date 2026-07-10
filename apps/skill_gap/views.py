import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import SkillGapAnalysis
from ai.services import analyze_skill_gap
from apps.dashboard.models import UserStat

@csrf_exempt
@login_required
def analyze_gap(request):
    if request.method == 'POST':
        try:
            target_role = "Generalist"
            current_skills = []
            
            if hasattr(request.user, 'profile'):
                target_role = request.user.profile.dream_role or "Generalist"
                # technical_skills might be a list of objects or strings
                current_skills = request.user.profile.technical_skills
                
            ai_response = analyze_skill_gap(current_skills, target_role)
            
            if ai_response.get('success') is False:
                return JsonResponse(ai_response)
                
            # Clear old
            SkillGapAnalysis.objects.filter(user=request.user).delete()
            
            # Save new
            gap = SkillGapAnalysis.objects.create(
                user=request.user,
                target_role=target_role,
                analysis_data=ai_response
            )
            
            # Update user stats
            stat, _ = UserStat.objects.get_or_create(user=request.user)
            # Calculate skills strength based on missing skills ratio
            total_skills = len(ai_response.get('current_skills_validated', [])) + len(ai_response.get('missing_skills', []))
            if total_skills > 0:
                strength = int((len(ai_response.get('current_skills_validated', [])) / total_skills) * 100)
                stat.skills_strength = strength
                stat.save()
            
            return JsonResponse({'success': True, 'analysis': gap.analysis_data})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
            
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def index(request):
    gap = SkillGapAnalysis.objects.filter(user=request.user).first()
    
    if gap and gap.analysis_data:
        skill_gap_json = gap.analysis_data
    else:
        skill_gap_json = {
            'match_pct': 0,
            'match_label': 'Not Analyzed',
            'match_change': '0%',
            'skills_have': 0,
            'skills_improve': 0,
            'skills_lack': 0,
            'target_role': {
                'title': getattr(request.user.profile, 'dream_role', 'Generalist') if hasattr(request.user, 'profile') else 'Generalist',
                'industry': 'Technology',
                'experience': 'Entry Level',
                'match_pct': 0,
                'total_required': 0,
                'have': 0,
                'improve': 0,
                'lack': 0
            },
            'breakdown': [],
            'top_gaps': [],
            'next_steps': []
        }
        
    return render(request, 'skill_gap/index.html', {'skill_gap_json': json.dumps(skill_gap_json)})
