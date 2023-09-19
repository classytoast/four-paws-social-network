from django.urls import path, re_path

from .views import *


urlpatterns = [
    path('animals/', SearchAnimalsView.as_view(), name='searching_animals'),
    path('owners/', SearchOwnersView.as_view(), name='searching_owners'),
    path('groups/', SearchGroupsView.as_view(), name='searching_groups'),
]
