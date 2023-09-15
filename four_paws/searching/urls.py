from django.urls import path

from .views import *


urlpatterns = [
    path('animals/', SearchAnimalsView.as_view(), name='searching_animals'),
    path('owners/', SearchOwnersView.as_view(), name='searching_owners'),
]
