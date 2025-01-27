from django.urls import path
from apps.boards.views.posts import (
    PostCreateListView,
    PostRetrieveUpdateDeleteView,
)

urlpatterns = [
    path("posts", PostCreateListView.as_view()),
    path("posts/<int:post_id>", PostRetrieveUpdateDeleteView.as_view()),
]
