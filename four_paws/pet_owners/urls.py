from django.urls import path

from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('profile/<int:id>/', ProfileHome.as_view(all_animals=False),
         name='profile_home'),
    path('profile/<int:id>/all-animals/', ProfileHome.as_view(all_animals=True),
         name='profile_with_all_animals'),
    path('change-follower/<int:animal_id>/', add_or_del_follower_for_animal,
         name='change_follower_for_animal'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]
