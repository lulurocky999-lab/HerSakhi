import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Resume
from ai.utils import extract_text_from_pdf
from ai.services import analyze_resume
from apps.dashboard.models import UserStat

@csrf_exempt
@login_required
def upload_resume(request):
    if request.method == 'POST':
        file = request.FILES.get('resume')
        if not file:
            return JsonResponse({'success': False, 'message': 'No file uploaded'})
            
        # Create Resume object
        resume = Resume.objects.create(
            user=request.user,
            file=file
        )
        
        # Extract Text
        text = extract_text_from_pdf(resume.file.path)
        resume.extracted_text = text
        resume.save()
        
        # Determine target role
        target_role = "Generalist"
        if hasattr(request.user, 'profile') and request.user.profile.dream_role:
            target_role = request.user.profile.dream_role
            
        # Call AI
        ai_response = analyze_resume(text, target_role)
        
        if ai_response.get('success') is False:
            return JsonResponse(ai_response)
            
        resume.ai_analysis = ai_response
        resume.ats_score = ai_response.get('ats_score', 0)
        resume.save()
        
        # Update User Profile resume text
        if hasattr(request.user, 'profile'):
            request.user.profile.resume_text = text
            request.user.profile.save()
            
        # Update Dashboard Stats (Lightweight sync)
        stat, created = UserStat.objects.get_or_create(user=request.user)
        # Bumping profile progress
        if stat.profile_progress < 100:
            stat.profile_progress = min(100, stat.profile_progress + 15)
        stat.save()
            
        return JsonResponse({
            'success': True,
            'ats_score': resume.ats_score,
            'analysis': resume.ai_analysis
        })
        
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def index(request):
    resume = Resume.objects.filter(user=request.user).first()
    
    if resume and resume.ai_analysis:
        resume_json = resume.ai_analysis
        resume_json['ats_score'] = resume.ats_score
    else:
        resume_json = {
            "ats_score": 0,
            "score_breakdown": {
                "format": 0, "content": 0, "skills": 0, "experience": 0, "keywords": 0
            },
            "strengths": [],
            "improvements": [],
            "keyword_match": 0,
            "target_role": getattr(request.user.profile, 'dream_role', 'Generalist') if hasattr(request.user, 'profile') else 'Generalist',
            "suggestions": [],
            "parsed_resume": {
                "name": "",
                "role": "",
                "email": "",
                "phone": "",
                "location": "",
                "linkedin": "",
                "github": "",
                "summary": "",
                "skills": [],
                "experience": [],
                "education": []
            }
        }
        
    return render(request, 'resume_lab/index.html', {
        'resume_json': json.dumps(resume_json),
        'resume': resume
    })
