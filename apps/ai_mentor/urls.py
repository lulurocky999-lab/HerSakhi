from django.urls import path
from . import views

app_name = 'ai_mentor'

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat_endpoint, name='chat_endpoint'),
    path('history/', views.chat_history, name='chat_history'),
    path('new/', views.new_conversation, name='new_conversation'),
    path('conversations/', views.conversation_list, name='conversation_list'),
]
