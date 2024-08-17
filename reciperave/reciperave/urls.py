from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.conf.urls import handler404

handler404 = 'users.views.custom_404'

urlpatterns = [
    path('', include('admin_panel.urls')),
    path('', include('users.urls')),
    path('', include('feedback.urls')),
    path('', include('recipes.urls')),
    path('', include('follows.urls')),
    path('', include('profiles.urls')),
    path('', include('search.urls')),
    path('', include('interactions.urls')),
    path('', include('bookmarks.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += staticfiles_urlpatterns()