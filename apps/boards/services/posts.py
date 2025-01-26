from apps.common.services import BaseService
from apps.boards.models.posts import Post
from apps.boards.validations.posts import CreatePost
from apps.boards.validations import exceptions


class CreatePostService(BaseService):
    model = Post

    def create_post(self, data: CreatePost) -> dict:
        post = Post(title=data.title, content=data.content, author_id=data.author_id)
        post.save()

        response_data = self._response_data_serializer(post=post)

        return response_data

    def _response_data_serializer(self, post: Post) -> dict:
        data = {
            "id": post.pk,
            "title": post.title,
            "content": post.content,
            "author_id": post.author_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
        }
        return data
