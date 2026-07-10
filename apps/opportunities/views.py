import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Opportunity, SavedOpportunity
from ai.services import extract_opportunities

@csrf_exempt
@login_required
def fetch_opportunities(request):
    if request.method == 'POST':
        try:
            profile_data = {}
            if hasattr(request.user, 'profile'):
                profile = request.user.profile
                profile_data = {
                    "dream_role": profile.dream_role,
                    "location": request.user.location,
                    "technical_skills": profile.technical_skills,
                    "preferred_industry": profile.preferred_industry,
                    "preferred_work_type": profile.preferred_work_type
                }
                
            ai_response = extract_opportunities(profile_data)
            
            if ai_response.get('success') is False:
                return JsonResponse(ai_response)
                
            opps_data = ai_response.get('opportunities', [])
            
            # Optionally clear old or just return the data. We'll store them for persistence.
            Opportunity.objects.all().delete()
            
            created_opps = []
            for opp in opps_data:
                o = Opportunity.objects.create(
                    title=opp.get('title', 'Unknown Role'),
                    company=opp.get('company', 'Unknown Company'),
                    location=opp.get('location', 'Remote'),
                    opportunity_type=opp.get('type', 'Job'),
                    deadline=None # Can parse time_left if needed
                )
                created_opps.append({
                    'id': o.id,
                    'title': o.title,
                    'company': o.company,
                    'location': o.location,
                    'type': o.opportunity_type,
                    'time_left': opp.get('time_left', 'N/A')
                })
                
            return JsonResponse({'success': True, 'opportunities': created_opps})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
            
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def index(request):
    opps = Opportunity.objects.all()[:10]
    saved_opps = SavedOpportunity.objects.filter(user=request.user)
    saved_ids = set(saved_opps.values_list('opportunity_id', flat=True))
    
    recommended = []
    for opp in opps:
        recommended.append({
            'id': opp.id,
            'title': opp.title,
            'company': opp.company,
            'logo_url': f"https://logo.clearbit.com/{opp.company.replace(' ', '').lower()}.com",
            'tags': [opp.opportunity_type],
            'location': opp.location,
            'type': opp.opportunity_type,
            'time_left': 'N/A',
            'saved': opp.id in saved_ids,
            'applied': False
        })
        
    saved_data = []
    for so in saved_opps:
        saved_data.append({
            'id': so.opportunity.id,
            'title': so.opportunity.title,
            'company': so.opportunity.company,
            'logo_url': f"https://logo.clearbit.com/{so.opportunity.company.replace(' ', '').lower()}.com",
            'location': so.opportunity.location,
        })
        
    opportunities_json = {
        'metrics': {
            'recommended': opps.count(),
            'applied': 0,
            'shortlisted': saved_opps.count(),
            'offers': 0
        },
        'recommended': recommended,
        'saved': saved_data,
        'categories': [
            {'name': 'Software', 'count': opps.count(), 'pct': 100}
        ],
        'total_categories': opps.count(),
        'top_companies': []
    }
    
    return render(request, 'opportunities/index.html', {'opportunities_json': json.dumps(opportunities_json)})
