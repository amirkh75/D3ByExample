from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,logout, authenticate
from django.urls import reverse
from django.views.generic import ListView, DetailView
import sys


from .forms import SignUpForm, LoginForm
from .models import CustomUser, Profile


from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.http import HttpResponse



def signup(request):
    """Signup logic with email verification needs to set user active."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(sys.stderr, 'in sign up view.....')
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            """Email veryfication for user signup to be active and ability to be login."""
            """Active in activate function down here."""
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
    """Active with unique link that emailed to user."""
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

def login_view(request):
    """Login view , just active users can login."""
    form = LoginForm(data = request.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None: # if user exist
            #print(sys.stderr, user.email)
            login(request, user, backend='users.backends.CustomUserBackend')

            """if user redirect to login view from anothe view goes back to his/her way after login"""
            path_redirect = request.get_full_path().split('?next=',1)                   #good piece of code
            if '?next=' in request.get_full_path():# Redirecting After Login 
                return redirect(path_redirect[1])
            else:
                return redirect('pages:home')
                
                 
        return render(request, 'users/login.html', {'form': form, 'error_message': 'Email or Password is wrong!'})
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})



def logout_view(request):
    """logout view, redirect to login view"""
    logout(request)
    return redirect(reverse('users:login'))


class UsersListView(ListView):
    """Show list of all users."""

    queryset =CustomUser.objects.all()
    context_object_name = 'CustomUsers'
    paginate_by = 10
    template_name = 'users/list.html'


class UsersDetailView(DetailView): #todo  change to profile.
    """Show user detail, but can be user profile."""

    model = CustomUser

    context_object_name = 'CustomUser'
    queryset = CustomUser.objects.all()
    template_name = 'users/detail.html'



class UsersProfileDetailView(DetailView):
    """Show user profile."""
    
    model = Profile

    context_object_name = 'Profile'
    queryset = Profile.objects.all()
    template_name = 'users/profile.html'