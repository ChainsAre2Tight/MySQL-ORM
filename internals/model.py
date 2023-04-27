import internals.database_fields as database_fields
from internals.processor import GetDataProcessor, GetTableInfoProcessor, InsertDataProcessor, MigrationProcessor
from internals.connector import DBConnection
from config import Config
from internals.interfaces import _AbstractModel
from internals.dataobject import DataObject


class Model(_AbstractModel):
    class _Objects:
        _fields: dict[str: database_fields.Field]

        def __init__(self, m: _AbstractModel):
            self._model = m
            self._fields = self._model.fields

        def _get_data(self, f: dict | None):
            # create a processor that connects to a database
            connection = DBConnection(**Config.connection_data)
            processor = GetDataProcessor(self._model, connection, f=f)
            processor.get_data()
            # processor must return a list of objects
            data = processor.data
            return data

        def all(self) -> list[DataObject]:
            return self._get_data(f=None)

        def filter(self, f: dict) -> list[DataObject]:
            return self._get_data(f=f)

        def insert_data(self, data: list[DataObject], commit: bool):
            # create a processor that connects to a database
            connection = DBConnection(**Config.connection_data)
            processor = InsertDataProcessor(self._model, connection, data)
            processor.insert_data(commit=commit)

    class _Checker:
        _fields: dict
        _staged_changes = list()

        def __init__(self, m: _AbstractModel):
            self._model = m
            self._fields = self._model.fields

        def _get_data(self):
            # create a processor that connects to a database
            connection = DBConnection(**Config.connection_data)
            processor = GetTableInfoProcessor(self._model, connection)
            processor.get_data()
            # processor returns a list of objects
            data = processor.data
            data.pop(0)  # remove reference to 'id' field
            return data

        def get_changes(self) -> dict[str: list[dict]]:
            changes = {
                'odd': list(),
                'missing': list(),
            }

            # retrieve data about columns from table
            data = self._get_data()
            for column in data:
                column_data = column.data
                is_column_present = False
                for field_name, field in self._model.fields.items():
                    if column_data['Field'] == field_name and column_data['Type'] == field.sql_data_type:
                        is_column_present = True
                if not is_column_present:
                    changes['odd'].append({
                        'Field': column_data['Field'],
                        'Type': column_data['Type'],
                    })

            for field_name, field in self._model.fields.items():
                is_field_present = False
                for column in data:
                    column_data = column.data
                    if column_data['Field'] == field_name and column_data['Type'] == field.sql_data_type:
                        is_field_present = True
                if not is_field_present:
                    changes['missing'].append({
                        'Field': field_name,
                        'Type': field.sql_data_type,
                    })

            return changes

        def get_ordered_fields(self) -> list[dict[str: str]]:
            ordered_fields = []

            previous = 'id'
            for field_name, field in self._model.fields.items():
                ordered_fields.append({
                    'Field': field_name,
                    'Type': field.sql_data_type,
                    'Previous': previous,
                })
                previous = field_name

            return ordered_fields

        def check_if_table_is_relevant(self) -> bool:
            changes = self.get_changes()
            if changes == {
                'odd': list(),
                'missing': list()
            }:
                return True
            else:
                return False

        def stage_changes(self):
            changes = self.get_changes()

            list_of_changes = list()
            for odd_field in changes['odd']:
                # stage deletion
                list_of_changes.append(MigrationProcessor.stage_remove_column(self._model, odd_field))
            for missing_field in changes['missing']:
                # stage creation
                list_of_changes.append(MigrationProcessor.stage_add_column(self._model, missing_field))
            ordered_fields = self.get_ordered_fields()
            for field in ordered_fields:
                # stage column swap
                list_of_changes.append(MigrationProcessor.stage_swap_column(self._model, field))

            self._staged_changes = list_of_changes

        @property
        def staged_changes(self):
            return self._staged_changes

    objects: _Objects
    checker: _Checker

    def __init__(self):
        self.objects = self._Objects(self)
        self.checker = self._Checker(self)

    # TODO move this method to a migrator as it shouldn't be here
    def is_relevant(self):
        return self.checker.check_if_table_is_relevant()

    def add_data(self, data: list[DataObject], commit: bool = False):
        self.objects.insert_data(data=data, commit=commit)
