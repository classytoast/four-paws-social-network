from django.urls import path

from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('test/', ProfileHome.as_view(), name='profile_home'),
]
