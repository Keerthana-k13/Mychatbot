# forms.py placeholder
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ChatForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={"rows":2}), label="Your Message")

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]