from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pet_owners.urls')),
    path('groups/', include('groups.urls')),
]
