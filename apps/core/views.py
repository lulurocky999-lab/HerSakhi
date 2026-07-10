from django.shortcuts import render

def landing_page(request):
    """Render the main landing page."""
    return render(request, 'landing/index.html')
