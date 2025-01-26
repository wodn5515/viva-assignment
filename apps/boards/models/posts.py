from apps.common.models import DjongoTimeStampedModel
from djongo import models


class Post(DjongoTimeStampedModel):
    title = models.CharField(max_length=256)
    content = models.TextField()
    author = models.IntegerField(db_index=True)

    class Meta:
        db_table = "posts"
