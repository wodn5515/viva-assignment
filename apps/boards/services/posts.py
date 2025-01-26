from apps.common.services import BaseService
from apps.boards.models.posts import Post
from apps.boards.validations.posts import CreatePost
from apps.boards.validations import exceptions


class PostService(BaseService):
    model = Post

    def create_post(self, data: CreatePost) -> dict:
        post = Post(title=data.title, content=data.content, author_id=data.author_id)
        post.save()

        response_data = self._instance_serializer(post=post)

        return response_data

    def get_post_set(self, **filter):
        filter["is_deleted"] = 0
        queryset = self.get_queryset(**filter)
        response_data = self._list_data_serializer(queryset)
        return response_data

    def get_post(self, id: int):
        orm_filter = {"is_deleted": 0}
        instance = self.get_object(id=id, **orm_filter)
        response_data = self._instance_serializer(instance)
        return response_data

    def _instance_serializer(self, post: Post) -> dict:
        data = {
            "id": post.pk,
            "title": post.title,
            "content": post.content,
            "author_id": post.author_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
        }
        return data

    def _list_data_serializer(self, queryset):
        results = [self._instance_serializer(post) for post in queryset]
        return {"results": results}
