from django.db.models.base import ModelBase
from django.conf import settings


class BaseService:
    page_size = settings.DEFAULT_PAGE_SIZE

    def get_instance_by_id(self, id: int):
        instance = self.model.objects.get(id=id)
        response_data = self._instance_serializer(instance)
        return response_data

    def soft_delete_by_id(self, id: int):
        self.model.objects.filter(id=id).update(is_deleted=True)

    def hard_delete_by_id(self, id: int):
        self.model.objects.filter(id=id).delete()

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

        queryset = queryset[start:end]

        response_data = self._list_data_serializer(queryset)

        return response_data
