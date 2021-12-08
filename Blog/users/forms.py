from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomUserAuthenticationForm(AuthenticationForm):

    class Meta:
        model = CustomUser
        fields = ( 'email',)

class SignUpForm(CustomUserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', )

class LoginForm(forms.Form):

    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)