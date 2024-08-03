# urls.py

from django.urls import path
from .views import search_recipes

urlpatterns = [
    path('search/', search_recipes, name='search_recipes'),
    # Add other URL patterns as needed
]
