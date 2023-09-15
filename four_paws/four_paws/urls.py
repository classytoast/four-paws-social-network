from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from four_paws import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pet_owners.urls')),
    path('groups/', include('groups.urls')),
    path('animals/', include('animals.urls')),
    path('posts/', include('posts.urls')),
    path('comments/', include('comments.urls')),
    path('searching/', include('searching.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
