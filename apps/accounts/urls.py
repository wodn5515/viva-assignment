from django.urls import path
from apps.accounts.views.users import SignUpAPIView, LoginView

urlpatterns = [
    path("users/signup", SignUpAPIView.as_view()),
    path("users/login", LoginView.as_view()),
    # path("users/refresh"),
    # path("users/logout"),
]
