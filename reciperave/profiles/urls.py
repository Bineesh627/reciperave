from django.urls import path
from . import views

urlpatterns = [
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('settings/', views.settings, name='settings'),
    path('profile/<str:username>/', views.profile, name='profile'),
]
