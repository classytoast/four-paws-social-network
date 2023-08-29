from django.urls import path

from .views import *


urlpatterns = [
    path('my-groups/', GroupsHome.as_view(), name='my_groups'),
    path('create-group/', CreateGroup.as_view(), name='create_group'),
    path('change-follower/<int:group_id>/', add_or_del_follower_for_group,
         name='change_follower_for_group'),
    path('<int:group_id>/', GroupView.as_view(), name='show_group'),
    path('<int:group_id>/create-group-post/', CreateGroupPostView.as_view(),
         name='create_group_post'),
    path('<int:group_id>/post/<int:post_id>/add-images-to-group-post/', AddGroupImgsView.as_view(),
         name='add_images_to_group_post'),
]