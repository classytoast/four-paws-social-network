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
    path('change-like-for-post/<int:post_id>/', put_or_remove_like_for_post,
         name='like_for_post'),
    path('profile/<int:id>/subscriptions/', OwnerSubscriptions.as_view(),
         name='owner_subscriptions'),
    path('personal-settings/<int:pk>/profile-settings/', UpdateOwner.as_view(),
         name='profile-settings'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]
