import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import MentorConversation, ChatMessage
from ai.services import chat_with_mentor
from apps.accounts.models import UserProfile
from django.core.serializers.json import DjangoJSONEncoder

from django.shortcuts import render

@login_required
def index(request):
    profile = getattr(request.user, 'profile', None)
    stat = getattr(request.user, 'dashboard_stat', None)

    conversations_qs = MentorConversation.objects.filter(user=request.user).order_by('-updated_at')[:5]
    conversation_count = MentorConversation.objects.filter(user=request.user).count()
    conversations = []
    for conv in conversations_qs:
        last_message = conv.messages.order_by('-timestamp').last()
        title = conv.title if conv.title else (last_message.content[:40] + '...' if last_message else 'Untitled conversation')
        time = last_message.timestamp.strftime('%b %d, %I:%M %p') if last_message else conv.updated_at.strftime('%b %d, %I:%M %p')
        conversations.append({
            'title': title,
            'time': time,
            'summary': last_message.content if last_message else ''
        })

    suggested_topics = []
    if profile:
        if profile.dream_role:
            suggested_topics.append(f"How can I improve my skills for {profile.dream_role}?")
        if profile.interests:
            suggested_topics.append(f"What projects should I build based on my interest in {profile.interests[0]}?")
        if profile.technical_skills:
            first_skill = profile.technical_skills[0].get('skill') if isinstance(profile.technical_skills[0], dict) else profile.technical_skills[0]
            if first_skill:
                suggested_topics.append(f"How can I strengthen my {first_skill} skills?")

    if not suggested_topics and conversation_count > 0:
        suggested_topics = [f"Continue the conversation about {conv['title']}" for conv in conversations[:3]]

    context = {
        'profile': profile,
        'stat': stat,
        'conversation_count': conversation_count,
        'conversations': conversations,
        'suggested_topics': suggested_topics,
    }
    return render(request, 'ai_mentor/index.html', context)

def _get_conversation(request):
    conversation_id = request.GET.get('conversation_id') or request.POST.get('conversation_id')
    if conversation_id:
        try:
            return MentorConversation.objects.get(id=conversation_id, user=request.user)
        except MentorConversation.DoesNotExist:
            pass
            
    # Get the most recent conversation or create a new one
    conversation = MentorConversation.objects.filter(user=request.user).order_by('-updated_at').first()
    if not conversation:
        conversation = MentorConversation.objects.create(user=request.user)
    return conversation

@login_required
def conversation_list(request):
    conversations = MentorConversation.objects.filter(user=request.user).order_by('-updated_at')
    conversation_data = []
    for conv in conversations:
        last_message = conv.messages.order_by('-timestamp').last()
        conversation_data.append({
            'id': conv.id,
            'title': conv.title or (last_message.content[:50] + '...' if last_message else 'Untitled conversation'),
            'updated_at': conv.updated_at,
            'message_count': conv.messages.count(),
            'preview': last_message.content if last_message else 'No messages yet.'
        })
    return render(request, 'ai_mentor/conversation_list.html', {'conversations': conversation_data})

@login_required
def new_conversation(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

    conversation = MentorConversation.objects.create(user=request.user)
    return JsonResponse({'success': True, 'conversation_id': conversation.id})

@login_required
def chat_history(request):
    conversation = _get_conversation(request)
    messages = conversation.messages.all().order_by('timestamp')
    data = [{'role': m.role, 'content': m.content} for m in messages]
    return JsonResponse({'success': True, 'history': data, 'conversation_id': conversation.id})

@csrf_exempt
@login_required
def chat_endpoint(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            attachment = data.get('attachment')
            
            if not user_message and not attachment:
                return JsonResponse({'success': False, 'message': 'Empty message'})
                
            # Use _get_conversation which correctly handles multiple conversations
            # First, temporarily attach the POST body JSON as if it were request.POST for _get_conversation
            request.POST = request.POST.copy()
            request.POST['conversation_id'] = data.get('conversation_id', '')
            conversation = _get_conversation(request)
            
            # If an attachment exists, merge its description with the user message for AI context.
            final_user_message = user_message
            if attachment:
                attachment_desc = f"Attached file: {attachment.get('file_name', 'unknown')} ({attachment.get('file_type', 'unknown')})."
                if attachment.get('content'):
                    attachment_desc += f" Content:\n{attachment.get('content')}"
                final_user_message = f"{final_user_message or ''}\n{attachment_desc}".strip()

            ChatMessage.objects.create(
                conversation=conversation,
                role='user',
                content=final_user_message
            )
            
            # Get history (last 10 messages for context window)
            messages = conversation.messages.all().order_by('-timestamp')[:10]
            history = [{'role': m.role, 'content': m.content} for m in reversed(messages)]
            
            # Build User Context
            user_context = {}
            if hasattr(request.user, 'profile'):
                profile = request.user.profile
                user_context = {
                    "dream_role": profile.dream_role,
                    "technical_skills": profile.technical_skills,
                    "soft_skills": profile.soft_skills,
                    "career_obstacles": profile.career_obstacles,
                }
            
            # Call AI
            ai_response = chat_with_mentor(history, final_user_message, user_context)
            
            if ai_response.get('success') is False or not ai_response.get('reply'):
                return JsonResponse({'success': False, 'message': 'AI is not available right now. Please try again later.'})
                
            reply = ai_response.get('reply')
            
            # Save assistant message
            ChatMessage.objects.create(
                conversation=conversation,
                role='assistant',
                content=reply
            )
            
            return JsonResponse({
                'success': True,
                'reply': reply,
                'suggested_actions': ai_response.get('suggested_actions', [])
            })
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in chat_endpoint: {e}", exc_info=True)
            return JsonResponse({'success': False, 'message': 'AI is not available right now. Please try again later.'})
            
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
