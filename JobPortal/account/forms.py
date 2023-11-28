from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class registerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['fullname', 'username', 'email', 'usertype']


class loginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=120)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['fullname', 'bio', 'resume']