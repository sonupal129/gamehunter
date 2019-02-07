from django import forms
from django.core.exceptions import ValidationError
from .models import *

class CheckoutForm(forms.Form):

    first_name = forms.CharField(max_length=18, widget=forms.TextInput(attrs={
        "placeholder": "First Name", }))
    last_name = forms.CharField(max_length=18, widget=forms.TextInput(attrs={
        "placeholder": "Last Name",
        }))
    mobile = forms.IntegerField(widget=forms.TextInput(attrs={
        "placeholder": "Mobile Number",
    }))
    shipping_address = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "placeholder": "Shipping Address", }))
    city = forms.CharField(max_length=25, widget=forms.TextInput(attrs={
        "placeholder": "City", }))
    state = forms.CharField(max_length=25, widget=forms.TextInput(attrs={
        "placeholder": "State", }))
    pincode = forms.IntegerField(widget=forms.TextInput(attrs={
        "placeholder": "Pincode",
    }))
