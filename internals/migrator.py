from internals.interfaces import _AbstractMigrator, _AbstractModel
# TODO update _AbstractModel to include all interface hints and update typehint for make_migrations
# from internals.model import Model
from abc import ABC, abstractmethod
from internals.interfaces import _AbstractMigratorProcessor

from internals.connector import DBConnection
from config import Config

from internals.processor import _AlterTableProcessor
from internals.processor import AddColumnProcessor, RemoveColumnProcessor, SwapColumnsProcessor


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


# TODO move this functions inside a proper processor
def stage_add_column(model, field):
    def perform_add_column(debug=False):
        connection = DBConnection(**Config.connection_data)
        processor = AddColumnProcessor(model, connection)
        processor.generate_sql(field)
        processor.perform(debug=debug)

    return perform_add_column


def stage_remove_column(model, field):
    def perform_delete_column(debug=False):
        connection = DBConnection(**Config.connection_data)
        processor = RemoveColumnProcessor(model, connection)
        processor.generate_sql(field)
        processor.perform(debug=debug)

    return perform_delete_column


def stage_swap_column(model, field):
    def perform_swap_columns(debug=False):
        connection = DBConnection(**Config.connection_data)
        processor = SwapColumnsProcessor(model, connection)
        processor.generate_sql(field)
        processor.perform(debug=debug)

    return perform_swap_columns
