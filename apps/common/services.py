from django.db.models.base import ModelBase


class BaseService:
    def get_instance_by_id(self, id: int):
        return self.model.objects.get(id=id)

    def soft_delete_by_id(self, id: int):
        self.model.objects.filter(id=id).update(is_deleted=True)

    def hard_delete_by_id(self, id: int):
        self.model.objects.filter(id=id).delete()

    def get_queryset(
        self, page: int | None, page_size: int, order_by: str | None, **filter
    ):
        queryset = self.models.objects.filter(**filter)
        if order_by:
            queryset = queryset.order_by(order_by)
        start, end = 0, page_size
        if page:
            start = (page - 1) * page_size
            end = page * page_size

        return queryset[start:end]
