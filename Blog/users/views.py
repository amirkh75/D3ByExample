from django.shortcuts import render, render, redirect, get_object_or_404
from django.contrib.auth import login,logout, authenticate
from django.urls import reverse
from django.views.generic import ListView, DetailView
import sys


from .forms import SignUpForm, LoginForm
from .models import CustomUser


from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.http import HttpResponse


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

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='users.backends.CustomUserBackend')
        return redirect('pages:home')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
# /////////////////////////////////////////////////////////////////////
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
            return redirect('pages:home')
        return render(request, 'users/login.html', {'form': form, 'error_message': 'Email or Password is wrong!'})
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect(reverse('users:login'))


class UsersListView(ListView):

    queryset =CustomUser.objects.all()
    context_object_name = 'CustomUsers'
    paginate_by = 10
    template_name = 'users/list.html'


class UsersDetailView(DetailView):

    context_object_name = 'CustomUser'
    queryset = CustomUser.objects.all()
    template_name = 'users/detail.html'
