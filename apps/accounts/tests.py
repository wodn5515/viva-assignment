from django.contrib.auth.models import User
from django.test import TestCase


class PostTestCase(TestCase):

    @classmethod
    def setUp(cls) -> None:
        cls.user_1 = User.objects.create(username="user_1")

    def test_댓글_목록을_조회한다(self):
        # 애니메이션 댓글 생성
        comment = Comment.objects.create(
            user=self.user_1, animation=self.ani_1, content="댓글 내용"
        )
        reported_comment = Comment.objects.create(
            user=self.user_2, animation=self.ani_1, content="댓글 내용"
        )
        # 댓글 신고 3회
        comment_reports = [
            CommentReport(comment=reported_comment, user=user, report_type="normal")
            for user in User.objects.all()
        ]
        CommentReport.objects.bulk_create(comment_reports)

        # 해당 애니메이션 댓글 목록 확인
        path = f"/comments?animation-id={self.ani_1.id}"
        response = self.client.get(path=path, content_type="application/json")

        # 애니메이션과 연결된 댓글이 1개 존재한다. (신고수가 3개 이상인 댓글은 조회 목록에서 제외)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], comment.id)
