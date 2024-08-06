# interactions/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('rate_and_comment/<int:recipe_id>/', views.rate_and_comment, name='rate_and_comment'),
    path('submit_rating_and_comment/<int:recipe_id>/', views.submit_rating_and_comment, name='submit_rating_and_comment'),
    path('edit_rating_and_comment/<int:recipe_id>/', views.edit_rating_and_comment, name='edit_rating_and_comment'),
]