from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # need to change the path
    path('', views.login_action, name='home'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('post', views.post_action, name='post'),
    path('followStream', views.followStream_action, name='followStream'),
    path('follower', views.follower_action, name='follower'),
    path('profile', views.profile_action, name='profile'),
]

