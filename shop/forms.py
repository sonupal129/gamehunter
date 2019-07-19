from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from shop.models import Product, Brand

class SignUpForm(forms.Form):
    email = forms.EmailField(max_length=30, required=True, widget=forms.EmailInput(attrs={
        "placeholder": "Email",
    }))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={
        "placeholder": "Enter Password",
    }))
    confirm_password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={
        "placeholder": "Enter Password",
    }))


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=40, widget=forms.TextInput(attrs={
        "placeholder": "Email"
    }))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        "placeholder": "Enter Password"
    }))


class PersonalDetailForm(forms.Form):

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        "placeholder": "First Name"
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        "placeholder": "Last Name"
    }))
    mobile = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        "placeholder": "Mobile"
    }))


class ChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        "placeholder": "Password"
    }))
    confirm_password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm Password"
    }))


class SellGamesForm(forms.Form):
    game_name = forms.CharField(max_length=18, widget=forms.TextInput(attrs={
        "placeholder": "Name of Game You want to Sell", }))
    game_type = forms.CharField(max_length=18, widget=forms.TextInput(attrs={
        "placeholder": "Name of Game You want to Sell", }))
    name = forms.CharField(max_length=18, widget=forms.TextInput(attrs={
        "placeholder": "Your Name",
    }))
    email = forms.EmailField(max_length=30, widget=forms.EmailInput(attrs={
        "placeholder": "Email",
    }))
    mobile = forms.IntegerField(widget=forms.TextInput(attrs={
        "placeholder": "Mobile Number",
    }))
    pickup_address = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "placeholder": "Pickup Address", }))
    city = forms.CharField(max_length=25, widget=forms.TextInput(attrs={
        "placeholder": "City", }))
    state = forms.CharField(max_length=25, widget=forms.TextInput(attrs={
        "placeholder": "State", }))
    pincode = forms.IntegerField(widget=forms.TextInput(attrs={
        "placeholder": "Pincode",
    }))


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(max_length=30, widget=forms.EmailInput(attrs={
        "placeholder": "Email",
    }))


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "developer", "publisher"]

class MyTestForm(forms.Form):
    developer = forms.ModelMultipleChoiceField(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
    publisher = forms.ModelMultipleChoiceField(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
    

