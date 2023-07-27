from django.urls import path

from .views import *


urlpatterns = [
    path('<int:post_id>/', ShowPost.as_view(), name='post'),
    path('create-post/', CreatePostView.as_view(), name='create_post'),
    path('<int:pk>/edit/', UpdatePostView.as_view(), name='edit_post'),
    path('<int:post_id>/add-images-to-post/', AddImgsView.as_view(),
         name='add-images-to-post'),
    path('<int:pk>/delete-post/', DeletePost.as_view(), name='delete_post'),
    path('<int:img_id>/delete-img/', delete_img, name='delete_image'),
]