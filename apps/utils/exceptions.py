from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import gettext_lazy as _


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("올바르지 않은 요청입니다.")
    default_code = "BAD_REQUEST"


class AuthenticationFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("ID/PW가 올바르지 않습니다.")
    default_code = "AUTHENTICATED_FAILED"


class NotAuthenticated(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("로그인이 필요합니다.")
    default_code = "NOT_AUTHENTICATED"


class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("권한이 없습니다.")
    default_code = "PERMISSION_DENIED"


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("요청한 데이터를 찾을 수 없습니다.")
    default_code = "NOT_FOUND"


class MethodNotAllowed(APIException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_detail = _("허용되지 않는 Method입니다.")
    default_code = "METHOD_NOT_ALLOWED"
