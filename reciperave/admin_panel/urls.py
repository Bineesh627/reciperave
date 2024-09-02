from django.contrib import admin
from django.urls import path
from admin_panel.views import CustomAdminLoginView

admin.site.site_header = 'RecipeRave admin'
admin.site.site_title = 'RecipeRave admin'
admin.site.index_title = 'RecipeRave administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/login/', CustomAdminLoginView.as_view(), name='admin_login'),
]