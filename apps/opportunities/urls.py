from django.urls import path
from . import views

app_name = 'opportunities'

urlpatterns = [
    path('', views.index, name='index'),
    path('match/', views.fetch_opportunities, name='match'),
]
