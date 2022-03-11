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

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user doesn't exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")
            if not user.is_active:
                raise forms.ValidationError("User no longer Active")
        return super(LoginForm,self).clean(*args,**kwargs)    