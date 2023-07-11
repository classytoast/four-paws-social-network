from django.urls import path

from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('profile/<int:id>/', ProfileHome.as_view(), name='profile_home'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]
