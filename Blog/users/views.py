from django.shortcuts import render, render, redirect
from django.contrib.auth import login,logout, authenticate
from .forms import SignUpForm, LoginForm
from django.urls import reverse
import sys


def profile_view(request):
    return render(request, 'profile.html')

def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)
        login(request, user)
        return redirect(reverse('pages:home'))
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})



def login_view(request):
    form = LoginForm(data = request.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        print(sys.stderr, 'user.email')
        print(sys.stderr, email)
        password = form.cleaned_data.get('password')
        print(sys.stderr, 'user.password')
        print(sys.stderr, password)
        user = authenticate(email=email, password=password)
        if user is not None:
            print(sys.stderr, user.email)
            login(request, user, backend='users.backends.CustomUserBackend')
        return redirect(reverse('pages:home'))
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect(reverse('users:login'))

