from django.urls import path

from .views import *


urlpatterns = [
    path('post/<int:post_id>/', ShowPost.as_view(), name='post'),
    path('create-post/', CreatePostView.as_view(), name='create_post'),
    path('post/<int:pk>/edit/', UpdatePostView.as_view(), name='edit_post'),
    path('add-images-to-post/<int:post_id>/', AddImgsView.as_view(),
         name='add-images-to-post'),
    path('delete-post/<int:post_id>/', delete_post, name='delete_post'),
    path('delete-img/<int:img_id>/', delete_img, name='delete_image'),
]