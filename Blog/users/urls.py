
from django.urls import path
from .views import signup_view, login_view, logout_view, UsersListView, UsersDetailView


app_name = 'users'

urlpatterns = [
    path('signup/', signup_view, name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('<int:pk>/', UsersDetailView.as_view(), name='user'),
    path('', UsersListView.as_view(), name='user_list'),
]

