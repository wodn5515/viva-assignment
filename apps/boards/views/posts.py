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
from apps.boards.services.posts import CreatePostService


class PostCreateRetrieveView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

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
