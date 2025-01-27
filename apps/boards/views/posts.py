from pydantic import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from apps.boards.validations.posts import CreatePost, UpdatePost
from apps.boards.validations import exceptions
from apps.boards.validations import exception_data
from apps.utils import exceptions as response_exceptions
from apps.utils import exception_data as common_exception_data
from apps.boards.services.posts import PostService
from datetime import datetime

POST_PAGE_SIZE = 10


class PostCreateListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        # validate
        try:
            page = int(self.request.GET.get("page", 1))
            page_size = int(self.request.GET.get("page-size", POST_PAGE_SIZE))
            order_by = self.request.GET.get("order-by", "newest")
            author_id = self.request.GET.get("author-id", None)
            if author_id:
                author_id = int(author_id)
        except ValueError:
            raise response_exceptions.BadRequest(
                **common_exception_data.HTTP_400_INPUT_VALIDATION_ERROR
            )

        queryset_kwargs = {
            "page": page,
            "page_size": page_size,
            "order_by": order_by,
        }
        if author_id:
            queryset_kwargs["author_id"] = author_id

        # service
        try:
            post_service = PostService()
            response_data = post_service.get_post_set(**queryset_kwargs)
        except exceptions.ValidationError:
            raise response_exceptions.BadRequest(
                **common_exception_data.HTTP_400_INPUT_VALIDATION_ERROR
            )

        return Response(status=status.HTTP_200_OK, data=response_data)

    def post(self, request, *args, **kwargs):
        request_data = request.data
        request_data["author_id"] = self.request.user.pk

        # validate
        try:
            data = CreatePost(**request_data)
        except exceptions.TitleTooLing:
            raise response_exceptions.BadRequest(
                **exception_data.HTTP_400_TITLE_TOO_LONG
            )
        except ValidationError:
            raise response_exceptions.BadRequest(
                **common_exception_data.HTTP_400_INPUT_VALIDATION_ERROR
            )

        # service
        post_service = PostService()
        response_data = post_service.create_post(data=data)

        return Response(status=status.HTTP_201_CREATED, data=response_data)


class PostRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id")

        # service
        try:
            post_service = PostService()
            response_data = post_service.get_post(id=post_id)
        except response_exceptions.NotFound:
            raise response_exceptions.NotFound(**exception_data.HTTP_404_POST_NOT_FOUND)

        return Response(status=status.HTTP_200_OK, data=response_data)

    def delete(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id")
        user = self.request.user

        # service
        try:
            post_service = PostService()
            post_service.check_ownership(
                user_id=user.pk, instance_id=post_id, user_field="author_id"
            )
            post_service.soft_delete_by_id(id=post_id)
        except response_exceptions.NotFound:
            raise response_exceptions.NotFound(**exception_data.HTTP_404_POST_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        request_data["updated_at"] = datetime.now()
        request_data["post_id"] = kwargs.get("post_id")
        request_data["request_user_id"] = self.request.user.pk

        # validate
        try:
            data = UpdatePost(**request_data)
        except exceptions.TitleTooLing:
            raise response_exceptions.BadRequest(
                **exception_data.HTTP_400_TITLE_TOO_LONG
            )
        except ValidationError:
            raise response_exceptions.BadRequest(
                **common_exception_data.HTTP_400_INPUT_VALIDATION_ERROR
            )

        # service
        try:
            post_service = PostService()
            response_data = post_service.update_post(data=data)
        except response_exceptions.NotFound:
            raise response_exceptions.NotFound(**exception_data.HTTP_404_POST_NOT_FOUND)

        return Response(status=status.HTTP_200_OK, data=response_data)
