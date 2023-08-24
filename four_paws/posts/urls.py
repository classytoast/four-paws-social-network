from django.urls import path

from .views import *


urlpatterns = [
    path('<int:post_id>/', ShowPost.as_view(), name='post'),
    path('create-post/', CreatePostView.as_view(), name='create_post'),
    path('<int:pk>/edit/', UpdatePostView.as_view(), name='edit_post'),
    path('<int:post_id>/add-images-to-post/', AddImgsView.as_view(),
         name='add_images_to_post'),
    path('<int:pk>/delete-post/', DeletePost.as_view(), name='delete_post'),
    path('<int:img_id>/delete-img/', delete_img, name='delete_image'),
    path('<int:post_id>/add-comment/', CreateComment.as_view(),
         name='add_comment'),
    path('<int:post_id>/<int:pk>/delete-comment/', DeleteComment.as_view(),
         name='delete_comment'),
    path('<int:post_id>/<int:pk>/edit-comment/', UpdateComment.as_view(),
         name='edit_comment'),
    path('<int:post_id>/change-like-for-comment/<int:comment_id>/',
         put_or_remove_like_for_comment, name='like_for_comment'),
]
