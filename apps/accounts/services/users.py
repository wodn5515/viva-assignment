from apps.common.services import BaseService
from apps.accounts.models.users import User
from apps.accounts.validations.users import (
    SignUpEntity,
    LoginEntity,
    RefreshTokenEntity,
)
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.validations import exceptions


class SignUpService(BaseService):
    model = User

    def create_user(self, data: SignUpEntity) -> dict:
        user = User(email=data.email, name=data.name)
        user.set_password(data.password)
        user.save()

        response_data = self._response_data_serializer(user=user)

        return response_data

    def _response_data_serializer(self, user=User) -> dict:
        data = {
            "id": user.pk,
            "name": user.name,
            "email": user.email,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
        return data


class LoginService:
    def login(self, data: LoginEntity):
        user = authenticate(email=data.email, password=data.password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            response_data = self._response_data_serializer(user=user, token=refresh)
            return response_data
        else:
            raise exceptions.EmailPasswordWrong

    def _response_data_serializer(self, user, token):
        data = {
            "user": self._user_serializer(user=user),
            "token": self._token_serializer(token=token),
        }
        return data

    def _user_serializer(self, user=User) -> dict:
        data = {
            "id": user.pk,
            "name": user.name,
            "email": user.email,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        }
        return data

    def _token_serializer(self, token):
        data = {"refresh": str(token), "access": str(token.access_token)}

        return data


class TokenRefreshService:
    def refresh(self, data: RefreshTokenEntity):
        refresh = RefreshToken(data.refresh)
        response_data = {"access": str(refresh.access_token)}
        return response_data


class LogoutService:
    def logout(self, data: RefreshTokenEntity):
        refresh = RefreshToken(data.refresh)
        refresh.blacklist()
