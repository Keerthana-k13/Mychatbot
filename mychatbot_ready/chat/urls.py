from django.urls import path
from . import views

urlpatterns = [
    path('', chat_views.home, name='home'),
    path('chat/', views.chat_view, name='chat'),  # Chat view
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', chat_views.register_view, name='register')
    path('profile/', views.profile_view, name='profile'),
]
