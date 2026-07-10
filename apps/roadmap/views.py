import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import CareerRoadmap, RoadmapMilestone
from ai.services import generate_career_roadmap
from apps.dashboard.models import Achievement

@csrf_exempt
@login_required
def generate_roadmap(request):
    if request.method == 'POST':
        try:
            # Build Context
            user_context = {}
            target_role = "Generalist"
            if hasattr(request.user, 'profile'):
                profile = request.user.profile
                target_role = profile.dream_role or "Generalist"
                user_context = {
                    "dream_role": profile.dream_role,
                    "technical_skills": profile.technical_skills,
                    "soft_skills": profile.soft_skills,
                    "resume_text": profile.resume_text,
                    "education": f"{profile.degree} - {profile.graduation_year}"
                }
                
            # Call AI
            ai_response = generate_career_roadmap(user_context)
            
            if ai_response.get('success') is False:
                return JsonResponse(ai_response)
                
            # Clear old roadmap
            CareerRoadmap.objects.filter(user=request.user).delete()
            
            # Create new roadmap
            roadmap = CareerRoadmap.objects.create(
                user=request.user,
                title=f"Path to {target_role}",
                target_role=target_role,
                estimated_finish=ai_response.get('estimated_finish', '6 months'),
                current_phase="Phase 1",
                completion_percentage=0
            )
            
            phases = ai_response.get('phases', [])
            for phase in phases:
                RoadmapMilestone.objects.create(
                    roadmap=roadmap,
                    title=phase.get('title', 'Unknown Phase'),
                    description=phase.get('description', ''),
                    order=phase.get('order', 0)
                )
                
            # Unlock Achievement
            Achievement.objects.get_or_create(
                user=request.user,
                title="Roadmap Generated",
                defaults={
                    "description": "Generated your first AI career roadmap.",
                    "icon": "map"
                }
            )
                
            return JsonResponse({'success': True, 'roadmap_id': roadmap.id})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
            
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
@login_required
def mark_milestone(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            milestone_id = data.get('milestone_id')
            is_completed = data.get('is_completed', True)
            
            milestone = RoadmapMilestone.objects.get(id=milestone_id, roadmap__user=request.user)
            milestone.is_completed = is_completed
            milestone.save()
            
            # Update roadmap progress
            roadmap = milestone.roadmap
            total = roadmap.milestones.count()
            completed = roadmap.milestones.filter(is_completed=True).count()
            
            if total > 0:
                roadmap.completion_percentage = int((completed / total) * 100)
                
            # Update current phase (first uncompleted)
            first_uncompleted = roadmap.milestones.filter(is_completed=False).order_by('order').first()
            if first_uncompleted:
                roadmap.current_phase = first_uncompleted.title
            else:
                roadmap.current_phase = "Completed"
                
            roadmap.save()
            
            return JsonResponse({
                'success': True, 
                'completion_percentage': roadmap.completion_percentage,
                'current_phase': roadmap.current_phase
            })
        except RoadmapMilestone.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Milestone not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
            
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def index(request):
    roadmap = CareerRoadmap.objects.filter(user=request.user).first()
    
    if roadmap:
        phases = []
        milestones = roadmap.milestones.all()
        for m in milestones:
            phases.append({
                'title': m.title,
                'description': m.description,
                'status': 'Completed' if m.is_completed else 'Pending',
                'tasks': [{'title': m.description, 'completed': m.is_completed}]
            })
            
        roadmap_json = {
            'role': roadmap.target_role,
            'timeframe': roadmap.estimated_finish,
            'est_completion': roadmap.estimated_finish,
            'overall_progress': roadmap.completion_percentage,
            'data': {
                'ahead_percentage': 68,
                'phases': phases
            }
        }
    else:
        roadmap_json = {
            'role': getattr(request.user.profile, 'dream_role', 'Generalist') if hasattr(request.user, 'profile') else 'Generalist',
            'timeframe': '6-12 Months',
            'est_completion': 'N/A',
            'overall_progress': 0,
            'data': {
                'ahead_percentage': 0,
                'phases': []
            }
        }
        
    return render(request, 'roadmap/index.html', {'roadmap_json': json.dumps(roadmap_json)})
