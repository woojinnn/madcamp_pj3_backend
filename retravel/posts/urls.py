from django.urls import path, include
from .apis import *

urlpatterns = [
    # Login not required
    # Get all posts
    path('api/posts/all-posts', PostListView.as_view()),

    path('api/posts/top-liked-posts', get_top_like_posts),
    path('api/posts/top-liked-cities', get_top_like_cities),
    path('api/posts/get-city-posts/<str:city>', get_city_posts),

    # Create a Post
    # Login required
    path('api/posts/create-post', create_post),

    # modify(PUT) or delete(DELETE) post with post_id
    # login required
    path('api/posts/modify/<int:post_id>', PostModification.as_view()),

    # login required
    # like, unlike
    path('api/posts/like/<int:post_id>', post_like),
    path('api/posts/unlike/<int:post_id>', post_unlike),

    # login required
    # get user's post
    path('api/posts/get-user-post', get_user_post_without_city),
    path('api/posts/get-user-post/<str:city>', get_user_post_with_city),

    # login required
    # get user's traveled cities
    path('api/posts/get-traveld-cities', get_user_traveld_cities),
]