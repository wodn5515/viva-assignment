from django.test import TestCase
from apps.accounts.models.users import User


class PostTestCase(TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.user1 = cls.create_user(
            cls, email="test1@test.com", name="테스트1", password="testpassword1"
        )
        cls.user2 = cls.create_user(
            cls, email="test2@test.com", name="테스트2", password="testpassword2"
        )
        cls.user3 = cls.create_user(
            cls, email="test3@test.com", name="테스트3", password="testpassword3"
        )
        cls.user4 = cls.create_user(
            cls, email="test4@test.com", name="테스트4", password="testpassword4"
        )
        cls.user5 = cls.create_user(
            cls, email="test5@test.com", name="테스트5", password="testpassword5"
        )

    def create_user(self, email, name, password):
        user = User(email=email, name=name)
        user.set_password(raw_password=password)
        user.save()
        return user

    def test_create_post_with_login(self):
        # 게시글 정보
        title = "test post title"
        content = "Lorem ipsum dolor"

        # 게시글 작성
        path = "/posts"
        request_data = {"title": title, "content": content}
        self.client.force_login(user=self.user1)
        response = self.client.post(
            path=path, data=request_data, content_type="application/json"
        )

        # 검증
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], title)
        self.assertEqual(response.data["content"], content)
        self.assertEqual(response.data["author_id"], self.user1.pk)

    def test_create_post_without_login(self):
        # 게시글 정보
        title = "test post title"
        content = "Lorem ipsum dolor"

        # 게시글 작성
        path = "/posts"
        request_data = {"title": title, "content": content}
        response = self.client.post(
            path=path, data=request_data, content_type="application/json"
        )

        # 검증
        self.assertEqual(response.status_code, 401)
