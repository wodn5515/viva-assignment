from pydantic import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from apps.boards.validations.posts import CreatePost
from apps.boards.validations import exceptions
from apps.boards.validations import exception_data
from apps.utils import exceptions as response_exceptions
from apps.utils import exception_data as common_exception_data
from apps.boards.services.posts import CreatePostService, RetrievePostsService

POST_PAGE_SIZE = 10


class PostCreateRetrieveView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        page = int(self.request.GET.get("page", 1))
        page_size = int(self.request.GET.get("page-size", POST_PAGE_SIZE))
        order_by = "-id"
        author_id = self.request.GET.get("author-id", None)

        queryset_kwargs = {
            "page": page,
            "page_size": page_size,
            "order_by": order_by,
        }
        if author_id:
            queryset_kwargs["author_id"] = author_id

        # service
        retrieve_posts_service = RetrievePostsService()
        response_data = retrieve_posts_service.get_queryset(**queryset_kwargs)

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
        create_post_service = CreatePostService()
        response_data = create_post_service.create_post(data=data)

        return Response(status=status.HTTP_201_CREATED, data=response_data)


class PostDetailUpdateDeleteView(APIView):
    pass
