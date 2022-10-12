from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']


class UpdateUserDetailsForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': 'Введенные пароли не совпадают',
    }
    first_name = forms.CharField(
        label='Имя',
        max_length=50,
        required=False,
        widget=forms.TextInput
    )
    email = forms.EmailField(
        label='Email',
        max_length=254,
        required=False,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )
    new_password1 = forms.CharField(
        label='Gfhjkm',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        required=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='Ведите пароль еще раз',
        strip=False,
        required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        if password2:
            password_validation.validate_password(password2, self.user)
        return password2

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if password1:
            password_validation.validate_password(password1, self.user)
        return password1

    def save(self, commit=True):
        password = self.cleaned_data.get('new_password1')
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        if password:
            self.user.set_password(password)
        if email:
            self.user.email = email
        if first_name:
            self.user.first_name = first_name
        if commit:
            self.user.save()
        return self.user
