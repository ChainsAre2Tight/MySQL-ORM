from internals.interfaces import _AbstractMigrator, _AbstractModel


class Migrator(_AbstractMigrator):
    migrations = []

    def make_migrations(self, list_of_models: list[_AbstractModel]):
        for model in list_of_models:
            pass

    def migrate(self):
        for i in range(len(self.migrations)):
            change = self.migrations.pop(0)
            change()
