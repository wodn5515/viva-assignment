from django.db import models
from apps.common.models import TimeStampedModel


class Post(TimeStampedModel):
    title = models.CharField(max_length=256)
    content = models.TextField()

    class Meta:
        db_table = "posts"
        app_label = "boards"
