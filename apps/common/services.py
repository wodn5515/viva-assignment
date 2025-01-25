from django.db.models.base import ModelBase


class BaseService:
    def get_instance_by_id(self, id: int):
        return self.model.objects.get(id=id)

    def soft_delete_by_id(self, id: int):
        self.model.objects.filter(id=id).update(is_deleted=True)

    def hard_delete_by_id(self, id: int):
        self.model.objects.filter(id=id).delete()
