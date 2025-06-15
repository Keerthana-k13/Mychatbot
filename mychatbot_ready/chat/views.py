from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from .models import ChatMessage

import openai

# Set up your OpenAI API key
openai.api_key = settings.OPENAI_API_KEY


# --- Local fallback chatbot logic ---
def local_bot_response(user_message):
    user_message = user_message.lower()

    if "hello" in user_message or "hi" in user_message:
        return "Hi there! I'm your backup bot. How can I help?"

    elif "your name" in user_message:
        return "I'm your local assistant when OpenAI is unavailable!"

    elif "bye" in user_message:
        return "Goodbye! I'm here whenever you need me."

    elif "help" in user_message:
        return "Sure! You can ask about features, project, or anything simple."

    else:
        return "Hmm... I didn't quite get that, but I'm here to help!"


# --- Chat view ---
@login_required
def chat_view(request):
    fallback_used = False  # Flag to track if OpenAI failed

    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()

        if user_message:
            try:
                # Try OpenAI API
                response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=[
                        {'role': 'user', 'content': user_message}
                    ]
                )
                ai_reply = response['choices'][0]['message']['content'].strip()

            except Exception as e:
                ai_reply = local_bot_response(user_message)
                ai_reply += "\n\n(Note: OpenAI is currently unavailable, so you're chatting with the local bot.)"
                fallback_used = True

            # Save chat
            ChatMessage.objects.create(
                user=request.user,
                message=user_message,
                response=ai_reply
            )

        return redirect('chat')

    # Fetch messages
    messages = ChatMessage.objects.filter(user=request.user).order_by('-timestamp')[:20]
    return render(request, 'chat/chat.html', {
        'messages': messages,
        'fallback_used': fallback_used
    })


# --- Home view ---
def home(request):
    return render(request, 'chat/home.html')

from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'chat/login.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')
from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Optional: Auto-login after registration
        login(request, user)
        return redirect('chat')

    return render(request, 'chat/register.html')
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    return render(request, 'chat/profile.html')