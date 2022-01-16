from django.urls import path, include
from .apis import *

urlpatterns = [
    path('api/posts/all-posts', PostListView.as_view()),
    # path('api/posts/user-posts', )

    path('api/posts/details/<int:post_id>', PostDetail.as_view()),

    path('api/posts/create-post', create_post),
    path('api/posts/update-post/', post_update_view),
    path('api/posts/delete-post/', post_delete_view),
]
