from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs = {'class':'input', 'size': '40'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs = {'class':'input', 'size': '40'}))
    choice = [('0', 'Public'), ('1', 'Private')]
    privacy = forms.ChoiceField(choices=choice, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs = {'class':'input', 'size': '40'}),
            'email': forms.EmailInput(attrs = {'class':'input', 'size': '40'}),
        }

