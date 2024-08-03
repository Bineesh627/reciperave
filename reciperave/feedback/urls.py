from django.urls import path
from . import views

urlpatterns = [
    path('feedback/', views.feedback, name='feedback'),
    path('feedbackForm/', views.feedbackForm, name='feedbackForm'),
    path('feedback_success/', views.feedback_success, name='feedback_success'),
]