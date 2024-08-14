from django.contrib import admin
from django.urls import path

admin.site.site_header = 'RecipeRave admin'
admin.site.site_title = 'RecipeRave admin'
admin.site.index_title = 'RecipeRave administration'

urlpatterns = [
    path('admin/', admin.site.urls),
]