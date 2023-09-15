from django.urls import path

from .views import *


urlpatterns = [
    path('animals/', SearchAnimalsView.as_view(),
         name='searching_animals'),
]
