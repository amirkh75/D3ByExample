from django.urls import path


from . import views
from .feeds import LatestPostsFeed


app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:user_id>', views.UserPostListView.as_view(), name='user_post_list'),
    path('commented/<int:user_id>', views.UserCommentedPostListView.as_view(), name='user_commented_post_list'),
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='post_list_by_tag'),
    #path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('create', views.PostCreateView.as_view(), name='post_create'),
]