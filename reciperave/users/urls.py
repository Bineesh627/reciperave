from django.urls import path
from users import views

urlpatterns = [
    path('home/', views.homes, name='homes'),
    path('', views.homes, name='homes'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
