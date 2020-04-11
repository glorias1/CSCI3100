from django import forms
from .models import userAccount

class LoginForm(forms.ModelForm):
    #username = forms.CharField(label='Username', max_length=30)
    #password = forms.CharField(label='Password', max_length=16)
    class Meta:
        model = userAccount
        fields = ('username','password')