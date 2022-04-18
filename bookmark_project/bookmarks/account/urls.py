from django.urls import path
from . import views



urlpatterns = [
    # account urls
    path('login/', views.user_login, name='login'),
]