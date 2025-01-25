class DBRouter:
    route_app_labels = ["boards"]

    db_name = "mongo"

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return self.db_name
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return self.db_name
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == self.db_name:
            return app_label in self.route_app_labels
        else:
            return app_label not in self.route_app_labels
