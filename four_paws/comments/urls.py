from django.urls import path

from .views import *


urlpatterns = [
    path('<int:post_id>/add-comment/<str:which_post>/', CreateComment.as_view(),
         name='add_comment'),
    path('<int:post_id>/<int:pk>/delete-comment/<str:which_post>/', DeleteComment.as_view(),
         name='delete_comment'),
    path('<int:post_id>/<int:pk>/edit-comment/<str:which_post>/', UpdateComment.as_view(),
         name='edit_comment'),
    path('<int:post_id>/change-like-for-comment/<int:comment_id>/<str:which_post>/',
         put_or_remove_like_for_comment, name='like_for_comment'),
]