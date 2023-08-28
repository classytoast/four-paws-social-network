from django.urls import path

from .views import *


urlpatterns = [
    path('my-groups/', GroupsHome.as_view(), name='my_groups'),
]