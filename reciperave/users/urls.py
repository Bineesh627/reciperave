from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.homes, name='homes'),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('error1/', views.error1, name='error'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
]
