from internals.interfaces import _AbstractMigrator, _AbstractModel


# TODO update _AbstractModel to include all interface hints and update typehint for make_migrations


class Migrator(_AbstractMigrator):
    migrations = []

    def make_migrations(self, list_of_models: list[_AbstractModel]):
        for model in list_of_models:
            model.checker.stage_changes()
            self.migrations.extend(model.checker.staged_changes)

    def migrate(self, debug=False):
        for i in range(len(self.migrations)):
            change = self.migrations.pop(0)
            change(debug)
