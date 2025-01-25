from django.urls import path
from apps.accounts.views.users import (
    SignUpAPIView,
    LoginView,
    LogoutView,
    TokenRefreshView,
)

urlpatterns = [
    path("users/signup", SignUpAPIView.as_view()),
    path("users/login", LoginView.as_view()),
    path("users/refresh", TokenRefreshView.as_view()),
    path("users/logout", LogoutView.as_view()),
]
