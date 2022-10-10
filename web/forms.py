from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']
