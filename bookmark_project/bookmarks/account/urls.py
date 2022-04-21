from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    # account urls
    #path('login/', views.user_login, name='login'),
    path('login/', 
        auth_views.LoginView.as_view(), name='login'),
    path('logout/',
        auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),

    # change password urls
    path('password_change/',
        auth_views.PasswordChangeView.as_view(),
        name='password_change'),
    path('password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
            # template_name='registration/password_reset_form.html',
            # form_class=CustomPasswordResetForm),
        name='password_change_done'),

    # reset password urls
    path('password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'),
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
    
    # registration
    path('register/', views.register, name='register'),

    # edit the user object and profile
    path('edit/', views.edit, name='edit'),
]