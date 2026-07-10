from django.urls import path
from . import views

app_name = 'assessment'

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit_assessment, name='submit_assessment'),
]
