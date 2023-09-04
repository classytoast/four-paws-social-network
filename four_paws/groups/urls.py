from django.urls import path

from .views import *


urlpatterns = [
    path('my-groups/', GroupsHome.as_view(), name='my_groups'),
    path('create-group/', CreateGroup.as_view(), name='create_group'),
    path('change-group-follower/<int:group_id>/', add_or_del_follower_for_group,
         name='change_follower_for_group'),
    path('<int:group_id>/', GroupView.as_view(), name='show_group'),
    path('<int:group_id>/<int:post_id>/', ShowGroupPost.as_view(), name='group_post'),
    path('<int:group_id>/create-group-post/', CreateGroupPostView.as_view(),
         name='create_group_post'),
    path('<int:group_id>/post/<int:post_id>/add-images-to-group-post/', AddGroupImgsView.as_view(),
         name='add_images_to_group_post'),
    path('<int:group_id>/<int:pk>/edit/', UpdateGroupPostView.as_view(), name='edit_group_post'),
    path('<int:group_id>/<int:pk>/delete-post/', DeleteGroupPost.as_view(), name='delete_group_post'),
    path('<int:group_id>/<int:img_id>/delete-img/', delete_img_for_group_post, name='delete_image_in_gp'),
    path('<int:group_id>/members/', GroupMembersView.as_view(), name='group_members'),
]