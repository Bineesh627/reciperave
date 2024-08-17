from django.urls import path
from users import views

urlpatterns = [
    path('home/', views.homes, name='homes'),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('auth/', views.signin_signup, name='signin_signup'),
    path('logout/', views.user_logout, name='logout'),
]
