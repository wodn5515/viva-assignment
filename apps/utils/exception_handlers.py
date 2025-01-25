from django.http import Http404
from rest_framework import exceptions
from apps.utils import exceptions as custom_exceptions
from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.views import set_rollback
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = custom_exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = custom_exceptions.PermissionDenied()
    elif isinstance(exc, InvalidToken):
        exc = custom_exceptions.NotAuthenticated()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        data = {
            "status": exc.status_code,
            "code": exc.get_codes(),
            "detail": exc.detail,
        }

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None
