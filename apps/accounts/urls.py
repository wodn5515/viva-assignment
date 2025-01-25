from django.urls import path
from apps.accounts.views.users import SignUpAPIView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("users/signup", SignUpAPIView.as_view()),
    path("users/login", LoginView.as_view()),
    path("users/refresh", TokenRefreshView.as_view()),
    # path("users/logout"),
]
