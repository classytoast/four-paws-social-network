from django.urls import path

from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('profile/<int:id>/', ProfileHome.as_view(all_animals=False),
         name='profile_home'),
    path('profile/<int:id>/all-animals/', ProfileHome.as_view(all_animals=True),
         name='profile_with_all_animals'),
    path('my-animals/', AnimalsHome.as_view(), name='all_animals_page'),
    path('post/<int:post_id>/', ShowPost.as_view(), name='post'),
    path('change-follower/<int:animal_id>/', add_or_del_follower_for_animal,
         name='change_follower_for_animal'),
    path('change-like-for-post/<int:post_id>/', put_or_remove_like_for_post,
         name='like_for_post'),
    path('create-post/', CreatePostView.as_view(), name='create_post'),
    path('post/<int:pk>/edit/', UpdatePostView.as_view(), name='edit_post'),
    path('add-images-to-post/<int:post_id>/', AddImgsView.as_view(),
         name='add-images-to-post'),
    path('delete-post/<int:post_id>/', delete_post, name='delete_post'),
    path('delete-img/<int:img_id>/', delete_img, name='delete_image'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]
