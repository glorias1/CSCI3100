from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')
    choice = [('Public', 'Public'), ('Private', 'Private')]
    privacy = forms.ChoiceField(choices=choice, widget=forms.RadioSelect)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'privacy',)