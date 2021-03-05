from django import forms
from django.contrib.auth.models import User
from store.models import Customer

class UserForm(forms.ModelForm):
    password=forms.CharField(max_length=32,widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username',"email","password")

class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ("phone",)
