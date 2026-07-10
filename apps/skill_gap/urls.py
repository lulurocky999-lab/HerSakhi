from django.urls import path
from . import views

app_name = 'skill_gap'

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.analyze_gap, name='analyze'),
]
