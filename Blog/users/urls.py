
from django.urls import path
from django.conf.urls import url
from .views import signup_view, login_view, logout_view, UsersListView, UsersDetailView, activate, signup


app_name = 'users'

urlpatterns = [
    #path('signup/', signup_view, name="signup"),
    path('signup/', signup, name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('<int:pk>/', UsersDetailView.as_view(), name='user'),
    #pathurl(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    activate, name='activate'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('', UsersListView.as_view(), name='user_list'),
]

