from apps.common.models import DjongoTimeStampedModel
from djongo import models


class Post(DjongoTimeStampedModel):
    title = models.CharField(max_length=256)
    content = models.TextField()
    author_id = models.IntegerField(db_index=True)
    is_deleted = models.IntegerField(default=0)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "posts"
