from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [

    # The home page
    path('', views.home, name='home'),

]


