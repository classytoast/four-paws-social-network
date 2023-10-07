from django.urls import path

from .views import *


urlpatterns = [
    path('<int:post_id>/<str:type_of_post>/', ShowPost.as_view(), name='post'),
    path('create-owner-post/', CreateOwnerPostView.as_view(), name='create_owner_post'),
    path('create-group-post/<int:group_id>', CreateGroupPostView.as_view(), name='create_group_post'),
    path('<int:pk>/edit/', UpdatePostView.as_view(), name='edit_post'),
    path('<int:post_id>/add-images-to-post/', AddImgsView.as_view(),
         name='add_images_to_post'),
    path('<int:pk>/delete-post/', DeletePost.as_view(), name='delete_post'),
    path('<int:img_id>/delete-img/', delete_img, name='delete_image'),
]
