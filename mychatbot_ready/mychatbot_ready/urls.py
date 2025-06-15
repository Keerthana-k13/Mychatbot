from django.contrib import admin
from django.urls import path
from chat import views as chat_views

urlpatterns = [
    path('', chat_views.home, name='home'),
    path('chat/', chat_views.chat_view, name='chat'),
    path('login/', chat_views.login_view, name='login'),
    path('logout/', chat_views.logout_view, name='logout'),  # Make sure this comma is present
    path('register/', chat_views.register_view, name='register'),  # <-- This caused the SyntaxError
    path('admin/', admin.site.urls),
    path('profile/', chat_views.profile_view, name='profile'),
]