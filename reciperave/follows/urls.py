from django.urls import path
from .views import followers, followings, follow_user, unfollow_user

urlpatterns = [
    path('profile/followers/<str:username>', followers, name='followers'),
    path('profile/followings/<str:username>', followings, name='followings'),
    path('follow/', follow_user, name='follow_user'),
    path('unfollow/', unfollow_user, name='unfollow_user'),
]
