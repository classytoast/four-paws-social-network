from django.urls import path

from .views import *


urlpatterns = [
    path('my-animals/', AnimalsHome.as_view(), name='all_animals_page'),
    path('<int:pk>/posts/', AnimalPosts.as_view(), name='animal_posts'),
    path('<int:pk>/followers/', AnimalFollowers.as_view(), name='animal_followers'),
    path('create-animal/', CreateAnimal.as_view(), name='create_animal'),
    path('<int:pk>/edit/', UpdateAnimal.as_view(), name='edit_animal'),
    path('<int:pk>/delete/', DeleteAnimal.as_view(), name='delete_animal'),
]
