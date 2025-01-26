from apps.utils.exceptions import NotFound, PermissionDenied
from django.conf import settings
from datetime import datetime


class BaseService:
    page_size = settings.DEFAULT_PAGE_SIZE

    def get_object(self, id: int, **filter):
        try:
            instance = self.model.objects.filter(**filter).get(id=id)
        except self.model.DoesNotExist:
            raise NotFound()
        return instance

    def update_object(self, id: int, filter: dict, **kwargs):
        self.model.objects.filter(id=id, **filter).update(**kwargs)

    def soft_delete_by_id(self, id: int):
        self.model.objects.filter(id=id).update(
            is_deleted=True, deleted_at=datetime.now()
        )

    def hard_delete_by_id(self, id: int):
        self.model.objects.filter(id=id).delete()

    def check_ownership(self, user_id: int, instance_id: int, user_field: str):
        instance = self.get_object(id=instance_id)
        if user_id != getattr(instance, user_field):
            raise PermissionDenied

    def get_queryset(
        self, page: int = 1, page_size: int = None, order_by: str = "-id", **filter
    ):
        if not page_size:
            page_size = self.page_size

        queryset = self.model.objects.filter(**filter)
        if order_by:
            queryset = queryset.order_by(order_by)

        start = (page - 1) * page_size
        end = page * page_size

        return queryset[start:end]
