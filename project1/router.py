class DatabaseRouter:
    def allow_relation(self, obj1, obj2, **hints):
        """
        Cho phép quan hệ giữa các objects ở các database khác nhau
        """
        return True  # Cho phép tất cả các quan hệ

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'customer':
            return 'customers'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'customer':
            return 'customers'
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'customer':
            return db == 'customers'
        return db == 'default'