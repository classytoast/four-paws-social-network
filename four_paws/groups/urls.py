from django.urls import path

from .views import *


urlpatterns = [
    path('my-groups/', GroupsHome.as_view(), name='my_groups'),
    path('create-group/', CreateGroup.as_view(), name='create_group'),
    path('change-follower/<int:group_id>/', add_or_del_follower_for_group,
         name='change_follower_for_group'),
]