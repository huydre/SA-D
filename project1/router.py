class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'book':
            return 'mongodb'
        elif model._meta.app_label == 'customer':
            return 'mysql'
        elif model._meta.app_label == 'order':
            return 'postgresql'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'book':
            return 'mongodb'
        elif model._meta.app_label == 'customer':
            return 'mysql'
        elif model._meta.app_label == 'order':
            return 'postgresql'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'book':
            return db == 'mongodb'
        elif app_label == 'customer':
            return db == 'mysql'
        elif app_label == 'order':
            return db == 'postgresql'
        return db == 'default'