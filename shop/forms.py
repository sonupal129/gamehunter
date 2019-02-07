from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(forms.Form):
    email = forms.EmailField(max_length=30, required=True, widget=forms.EmailInput(attrs={
        "placeholder": "Email",
    }))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
    }))


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=40, widget=forms.TextInput(attrs={
        "placeholder": "Username or Email"
    }))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        "placeholder": "Password"
    }))

