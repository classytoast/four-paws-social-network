from django.urls import path, re_path

from .views import *


urlpatterns = [
    # re_path(r'^animals/(?P<category_of_animal>[\w-]+)/$',
    path('animals/',
            SearchAnimalsView.as_view(), name='searching_animals'),
    path('owners/', SearchOwnersView.as_view(), name='searching_owners'),
    path('groups/', SearchGroupsView.as_view(), name='searching_groups'),
]
