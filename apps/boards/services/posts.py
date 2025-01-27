from apps.common.services import BaseService
from apps.boards.models.posts import Post
from apps.boards.validations.posts import CreatePost, UpdatePost
from apps.boards.validations import exceptions


class PostService(BaseService):
    model = Post

    def create_post(self, data: CreatePost) -> dict:
        post = Post(title=data.title, content=data.content, author_id=data.author_id)
        post.save()

        response_data = self._instance_serializer(post=post)

        return response_data

    def get_post_set(self, **filter):
        order_by = filter["order_by"]
        filter["order_by"] = self._convert_order_by(order_by)
        filter["is_deleted__in"] = [False]
        queryset = self.get_queryset(**filter)
        response_data = self._list_data_serializer(queryset)
        return response_data

    def get_post(self, id: int):
        orm_filter = {"is_deleted__in": [False], "id": id}
        instance = self.get_object(**orm_filter)
        response_data = self._instance_serializer(instance)
        return response_data

    def update_post(self, data: UpdatePost):
        self.check_ownership(
            user_id=data.request_user_id,
            instance_id=data.post_id,
            user_field="author_id",
        )
        update_keys = ["title", "content", "updated_at"]
        orm_filter = {"is_deleted__in": [False], "id": data.post_id}
        update_dict = self._set_update_dict(data=data, update_keys=update_keys)
        self.update_objects(filter=orm_filter, **update_dict)
        instance = self.get_object(**orm_filter)
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

    def _set_update_dict(self, data: UpdatePost, update_keys: list):
        update_dict = {}
        for key in data.__dict__:
            if key in update_keys:
                update_dict[key] = getattr(data, key)
        return update_dict

    def _convert_order_by(self, order_by: str) -> str:
        if order_by == "newest":
            result = "-id"
        elif order_by == "oldest":
            result = "id"
        else:
            raise exceptions.ValidationError
        return result
