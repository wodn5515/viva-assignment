from django.test import TestCase
from apps.accounts.models.users import User
from apps.boards.models.posts import Post
from apps.boards.views.posts import POST_PAGE_SIZE


class PostTestCase(TestCase):
    databases = "__all__"

    @classmethod
    def setUpTestData(cls) -> None:
        # 유저 더미데이터 생성
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
        cls.users = [cls.user1, cls.user2, cls.user3, cls.user4, cls.user5]

    def create_user(self, email, name, password):
        user = User(email=email, name=name)
        user.set_password(raw_password=password)
        user.save()
        return user

    def create_dummy_posts(self):
        posts = []
        for i in range(40):
            post = Post(
                title=f"test post title{i}",
                content=f"Lorem ipsum dolor{i}",
                author_id=self.users[i % len(self.users)].pk,
            )
            posts.append(post)

        Post.objects.bulk_create(posts)
        return posts

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

    def test_retrieve_posts(self):
        # 게시글 더미데이터 생성
        self.create_dummy_posts()

        # default
        # 게시글 목록 조회
        page_size = POST_PAGE_SIZE
        path = "/posts"
        response = self.client.get(path=path, content_type="application/json")

        # 검증용 데이터
        post = Post.objects.order_by("-id").first()

        # 검증
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), page_size)
        self.assertEqual(response.data["results"][0]["id"], post.pk)
        self.assertEqual(response.data["results"][0]["content"], post.content)

        # page filter
        # 게시글 목록 조회
        page_size = 5
        page = 2
        path = f"/posts?page={page}&page-size={page_size}"
        response = self.client.get(path=path, content_type="application/json")

        # 검증용 데이터
        post_set = Post.objects.order_by("-id")[5:10]

        # 검증
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), page_size)
        self.assertEqual(response.data["results"][0]["id"], post_set[0].pk)
        self.assertEqual(response.data["results"][0]["content"], post_set[0].content)

        # author_id filter
        # 게시글 목록 조회
        author_id = self.user1.pk
        page_size = POST_PAGE_SIZE
        path = f"/posts?author-id={author_id}&page_size={page_size}"
        response = self.client.get(path=path, content_type="application/json")

        # 검증용 데이터
        post_set = Post.objects.filter(author_id=author_id).order_by("-id")[:page_size]

        # 검증
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), len(post_set))
        self.assertEqual(response.data["results"][0]["id"], post_set[0].pk)
        self.assertEqual(response.data["results"][0]["content"], post_set[0].content)

        # page 초과시
        # 게시글 목록 조회
        page_size = POST_PAGE_SIZE
        page = 100
        path = f"/posts?page={page}&page-size={page_size}"
        response = self.client.get(path=path, content_type="application/json")

        # 검증
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 0)

    def test_read_post(self):
        # 게시글 더미데이터 생성
        self.create_dummy_posts()

        # 검증용 데이터
        post = Post.objects.first()
        # 게시글 조회
        path = f"/posts/{post.pk}"
        response = self.client.get(path=path, content_type="application/json")

        # 검증
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], post.pk)
        self.assertEqual(response.data["content"], post.content)

    def test_delete_post(self):
        # 게시글 더미데이터 생성
        self.create_dummy_posts()

        # 내 게시글
        # 삭제할 게시글
        post = Post.objects.filter(
            author_id=self.user1.pk, is_deleted__in=[False]
        ).first()

        # 게시글 삭제
        path = f"/posts/{post.pk}"
        self.client.force_login(user=self.user1)
        response = self.client.delete(path=path)

        # 검증
        self.assertEqual(response.status_code, 204)

        # 게시글이 삭제되었는지 확인
        response = self.client.get(path=path)

        # 검증
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["code"], "POST_NOT_FOUND")

        # 타인의 게시글
        # 삭제할 게시글
        post = Post.objects.filter(
            author_id=self.user2.pk, is_deleted__in=[False]
        ).first()

        # 게시글 삭제
        path = f"/posts/{post.pk}"
        response = self.client.delete(path=path)

        # 검증
        self.assertEqual(response.status_code, 403)

        # 게시글이 삭제되지않았는지 확인
        response = self.client.get(path=path)

        # 검증
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], post.pk)

        # 비로그인시
        self.client.logout()
        response = self.client.delete(path=path)

        # 검증
        self.assertEqual(response.status_code, 401)

        # 게시글이 삭제되지않았는지 확인
        response = self.client.get(path=path)

        # 검증
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], post.pk)

    def test_update_post(self):
        # 게시글 더미데이터 생성
        self.create_dummy_posts()

        # 로그인
        self.client.force_login(user=self.user1)

        # 내 게시글
        # 수정할 게시글
        post = Post.objects.filter(
            author_id=self.user1.pk, is_deleted__in=[False]
        ).first()

        # 게시글 수정
        updated_title = f"test update title {post.pk}"
        updated_content = f"update Lorem ipsum dolor {post.pk}"
        path = f"/posts/{post.pk}"
        request_data = {"title": updated_title, "content": updated_content}
        response = self.client.patch(
            path=path, data=request_data, content_type="application/json"
        )

        # 검증
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], updated_title)
        self.assertEqual(response.data["content"], updated_content)
        self.assertNotEqual(response.data["created_at"], response.data["updated_at"])

        # 타인의 게시글
        # 수정할 게시글
        post = Post.objects.filter(
            author_id=self.user2.pk, is_deleted__in=[False]
        ).first()

        # 게시글 수정
        updated_title = f"test update title {post.pk}"
        updated_content = f"update Lorem ipsum dolor {post.pk}"
        path = f"/posts/{post.pk}"
        request_data = {"title": updated_title, "content": updated_content}
        response = self.client.patch(
            path=path, data=request_data, content_type="application/json"
        )

        # 검증
        self.assertEqual(response.status_code, 403)

        # 게시글이 수정되지않았는지 확인
        response = self.client.get(path=path)

        # 검증
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data["title"], updated_title)

        # 비로그인시
        # 로그아웃
        self.client.logout()
        # 게시글 수정
        updated_title = f"test update title {post.pk}"
        updated_content = f"update Lorem ipsum dolor {post.pk}"
        path = f"/posts/{post.pk}"
        request_data = {"title": updated_title, "content": updated_content}
        response = self.client.patch(
            path=path, data=request_data, content_type="application/json"
        )

        # 검증
        self.assertEqual(response.status_code, 401)

        # 게시글이 수정되지않았는지 확인
        response = self.client.get(path=path)

        # 검증
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data["title"], updated_title)
