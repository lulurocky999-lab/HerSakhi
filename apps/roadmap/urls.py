from django.urls import path
from . import views

app_name = 'roadmap'

urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate_roadmap, name='generate'),
    path('mark-milestone/', views.mark_milestone, name='mark_milestone'),
]
