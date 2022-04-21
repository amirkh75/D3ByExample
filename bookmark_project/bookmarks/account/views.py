from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm


def user_login(request):
    """user log in view base on django user model."""
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})



from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    """You decorate your view with the login_required decorator of the authentication
        framework. The login_required decorator checks whether the current user is
        authenticated. If the user is authenticated, it executes the decorated view; if the
        user is not authenticated, it redirects the user to the login URL with the originally
        requested URL as a GET parameter named next."""
    return render(request,
                 'account/dashboard.html',
                 {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request,
                        'account/register_done.html',
                        {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                'account/register.html',
                {'user_form': user_form})
