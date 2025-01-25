from django.db.utils import IntegrityError
from pydantic import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.validations.users import SignUp, Login
from apps.accounts.services.users import SignUpService, LoginService
from apps.utils import exceptions as response_exceptions
from apps.accounts.validations import exceptions
from apps.accounts.validations import exception_data
from apps.utils import exception_data as common_exception_data


class SignUpAPIView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        request_data = request.data

        # validate
        try:
            data = SignUp(**request_data)
        except exceptions.PasswordNotMatched:
            raise response_exceptions.BadRequest(
                **exception_data.HTTP_400_PASSWORD_NOT_MATCHED
            )
        except ValidationError:
            raise response_exceptions.BadRequest(
                **common_exception_data.HTTP_400_INPUT_VALIDATION_ERROR
            )

        # service
        try:
            signup_service = SignUpService()
            response_data = signup_service.create_user(data=data)
        except IntegrityError:
            raise response_exceptions.BadRequest(
                **exception_data.HTTP_400_ALREADY_SIGNED_UP_EMAIL
            )

        return Response(status=status.HTTP_200_OK, data=response_data)


class LoginView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        request_data = request.data

        # validate
        try:
            data = Login(**request_data)
        except ValidationError:
            raise response_exceptions.BadRequest(
                **common_exception_data.HTTP_400_INPUT_VALIDATION_ERROR
            )

        # service
        try:
            login_service = LoginService()
            response_data = login_service.login(data)
        except exceptions.EmailPasswordWrong:
            raise response_exceptions.AuthenticationFailed()

        return Response(status=status.HTTP_200_OK, data=response_data)
