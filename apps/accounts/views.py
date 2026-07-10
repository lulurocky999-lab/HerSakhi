from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

def login_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:index')
        else:
            error = "Invalid email or password."
    return render(request, 'auth/login.html', {'error': error})

def signup_view(request):
    error = None
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=email).exists():
            error = "An account with this email already exists."
        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )
            login(request, user)
            return redirect('accounts:onboarding')
            
    return render(request, 'auth/signup.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('core:landing')

@login_required
def onboarding_view(request):
    if request.method == 'POST':
        user = request.user
        user.dream_career = request.POST.get('dream_career', '')
        user.save()
        return redirect('dashboard:index')
    return render(request, 'auth/onboarding.html')

@login_required
def profile_view(request):
    profile = getattr(request.user, 'profile', None)
    stats = getattr(request.user, 'dashboard_stat', None)
    achievements_count = request.user.achievements.count() if hasattr(request.user, 'achievements') else 0
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'stats': stats,
        'achievements_count': achievements_count,
    })

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
@require_POST
def profile_update_view(request):
    try:
        data = json.loads(request.body)
        user = request.user
        profile = getattr(user, 'profile', None)
        
        if not profile:
            from .models import UserProfile
            profile = UserProfile.objects.create(user=user)
            
        action = data.get('action')
        
        if action == 'basic_info':
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.location = data.get('location', user.location)
            user.save()
            
            profile.current_status = data.get('current_status', profile.current_status)
            profile.education_level = data.get('education_level', profile.education_level)
            profile.dream_role = data.get('dream_role', profile.dream_role)
            profile.save()
            return JsonResponse({'status': 'success'})
            
        elif action == 'about_me':
            profile.resume_text = data.get('resume_text', profile.resume_text)
            profile.save()
            return JsonResponse({'status': 'success'})
            
        elif action == 'skills':
            skills_str = data.get('skills', '')
            skills_list = [s.strip() for s in skills_str.split(',') if s.strip()]
            
            # Convert to list of dicts: {'skill': '...', 'proficiency': 'Intermediate'}
            formatted_skills = []
            for skill in skills_list:
                formatted_skills.append({
                    'skill': skill,
                    'proficiency': 'Intermediate' # default
                })
                
            profile.technical_skills = formatted_skills
            profile.save()
            return JsonResponse({'status': 'success'})
            
        return JsonResponse({'status': 'error', 'message': 'Unknown action'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
