from django.urls import path
from . import views

urlpatterns = [
    path('bookmark/<int:recipe_id>/', views.bookmark_recipe, name='bookmark'),
    path('bookmarks/', views.view_bookmark, name='view_bookmark'),
    path('unbookmark/<int:recipe_id>/', views.unbookmark_recipe, name='unbookmark'),
]
