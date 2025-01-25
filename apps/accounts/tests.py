from django.test import TestCase
from apps.accounts.models.users import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient


class AccountTestCase(TestCase):

    def test_signup(self):
        # 유저 정보
        email = "test@test.com"
        name = "testuser"
        password = "testpassword"
        wrong_password = "wrongtestpassword"

        # 회원가입
        path = "/users/signup"
        request_data = {
            "email": email,
            "name": name,
            "password": password,
            "password_check": password,
        }
        response = self.client.post(
            path=path, data=request_data, content_type="application/json"
        )

        # 검증
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], email)
        self.assertEqual(response.data["name"], name)
        self.assertTrue(response.data["is_active"])

        # 이미 가입된 이메일로 회원가입
        response = self.client.post(
            path=path, data=request_data, content_type="application/json"
        )

        # 검증
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], "ALREADY_SIGNED_UP_EMAIL")

        # 비밀번호가 서로 다른경우 회원가입
        request_data = {
            "email": email,
            "name": name,
            "password": password,
            "password_check": wrong_password,
        }
        response = self.client.post(
            path=path, data=request_data, content_type="application/json"
        )

        # 검증
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], "PASSWORD_NOT_MATCHED")

    def test_login(self):
        # 유저 정보
        email = "test@test.com"
        name = "testuser"
        password = "testpassword"
        wrong_password = "wrongtestpassword"

        # 유저 생성
        user = User(email=email, name=name)
        user.set_password(password)
        user.save()

        # 로그인
        path = "/users/login"
        request_data = {"email": email, "password": password}
        response = self.client.post(
            path=path, data=request_data, content_type="application/json"
        )

        # access token -> user
        jwt_authentication = JWTAuthentication()
        validated_token = jwt_authentication.get_validated_token(
            response.data["token"]["access"]
        )
        user_from_token = jwt_authentication.get_user(validated_token)

        # 검증
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user"]["id"], user.pk)
        self.assertEqual(response.data["user"]["name"], user.name)
        self.assertEqual(user_from_token.id, user.pk)

        # email/password 틀린 경우 로그인
        request_data = {"email": email, "password": wrong_password}
        response = self.client.post(
            path=path, data=request_data, content_type="application/json"
        )

        # 검증
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], "AUTHENTICATED_FAILED")

    def test_refresh_token(self):
        # 유저 정보
        email = "test@test.com"
        name = "testuser"
        password = "testpassword"

        # 유저 생성
        user = User(email=email, name=name)
        user.set_password(password)
        user.save()

        # refresh_token get
        refresh = RefreshToken.for_user(user)

        # refresh 토큰으로 access token 요청
        path = "/users/refresh"
        request_data = {"refresh": str(refresh)}
        response = self.client.post(
            path=path, data=request_data, content_type="application/json"
        )

        # access token -> user
        jwt_authentication = JWTAuthentication()
        validated_token = jwt_authentication.get_validated_token(
            response.data["access"]
        )
        user_from_token = jwt_authentication.get_user(validated_token)

        # 검증
        self.assertEqual(response.status_code, 200)
        self.assertTrue("access" in response.data)
        self.assertEqual(user_from_token.pk, user.pk)

    def test_logout(self):
        # 유저 정보
        email = "test@test.com"
        name = "testuser"
        password = "testpassword"

        # 유저 생성
        user = User(email=email, name=name)
        user.set_password(password)
        user.save()

        # 로그인
        path = "/users/login"
        request_data = {"email": email, "password": password}
        response = self.client.post(
            path=path, data=request_data, content_type="application/json"
        )
        refresh_token = response.data["token"]["refresh"]

        # 로그아웃
        path = "/users/logout"
        self.client.login(email=email, password=password)
        request_data = {"refresh": refresh_token}
        response = self.client.post(
            path=path, data=request_data, content_type="application/json"
        )
        self.client.logout()

        # 검증
        self.assertEqual(response.status_code, 204)

        # refresh token 무효화 검증을 위해 refresh 토큰으로 access token 요청
        path = "/users/refresh"
        request_data = {"refresh": refresh_token}
        response = self.client.post(
            path=path, data=request_data, content_type="application/json"
        )

        # 검증
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], "TOKEN_IS_INVALID_OR_EXPIRED")
