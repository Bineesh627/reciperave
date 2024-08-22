from django.urls import path
from . import views

urlpatterns = [
    path('upload_recipe/', views.upload_recipe, name='upload_recipe'),
    path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('view_recipe/<int:recipe_id>/', views.view_recipe, name='view_recipe'),
    path('delete_recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
]
