from django.urls import path
from apps.boards.views.posts import (
    PostCreateRetrieveView,
    PostDetailUpdateDeleteView,
)

urlpatterns = [
    path("posts", PostCreateRetrieveView.as_view()),
    path("posts/<int:post_id>", PostDetailUpdateDeleteView.as_view()),
]
