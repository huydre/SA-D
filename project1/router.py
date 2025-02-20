class DatabaseRouter:
    # Dictionary mapping apps to their databases
    APP_DB_MAPPING = {
        'book': 'mongodb',
        'customer': 'mysql',
        'order': 'postgresql',
        'shipping': 'postgresql',
        'paying': 'postgresql',
        'cart': 'postgresql',
        'cartitem': 'postgresql',
    }

    def _get_db(self, app_label):
        return self.APP_DB_MAPPING.get(app_label, 'default')

    def db_for_read(self, model, **hints):
        return self._get_db(model._meta.app_label)

    def db_for_write(self, model, **hints):
        return self._get_db(model._meta.app_label)

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        target_db = self._get_db(app_label)
        return db == target_db