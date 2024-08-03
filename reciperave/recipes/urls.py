# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload_recipe/', views.upload_recipe, name='upload_recipe'),
    path('upload_recipe_action/', views.upload_recipe_action, name='upload_recipe_action'),
    path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('edit_recipe_action/<int:recipe_id>/', views.edit_recipe_action, name='edit_recipe_action'),
    path('view_recipe/<int:recipe_id>/', views.view_recipe, name='view_recipe'),
    path('delete_recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
]
