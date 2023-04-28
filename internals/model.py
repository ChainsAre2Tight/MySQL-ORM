import internals.database_fields as database_fields
from internals.processor import GetDataProcessor, GetTableInfoProcessor, InsertDataProcessor, MigrationProcessor
from internals.connector import DBConnection
from config import Config
from internals.interfaces import _AbstractModel
from internals.dataobject import DataObject, FieldData


class Model(_AbstractModel):
    class _Objects(_AbstractModel._Objects):
        _fields: dict[str: database_fields.Field]

        def __init__(self, m: _AbstractModel):
            self._model = m
            self._fields = self._model.fields

        def _get_data(self, f: dict | None) -> list[DataObject]:
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

    class _Checker(_AbstractModel._Checker):
        _fields: dict
        _staged_changes = list()

        def __init__(self, m: _AbstractModel):
            self._model = m
            self._fields = self._model.fields

        def _get_data(self) -> list[FieldData]:
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
            columns = self._get_data()
            fields = self._model.get_list_of_fields()
            for column in columns:
                is_column_present = False
                for field in fields:
                    if field == column:
                        is_column_present = True
                if not is_column_present:
                    changes['odd'].append(column)

            for field in fields:
                is_field_present = False
                for column in columns:
                    if column == field:
                        is_field_present = True
                if not is_field_present:
                    changes['missing'].append(field)

            return changes

        def get_ordered_fields(self) -> list:
            ordered_fields = []
            list_of_fields = self._model.get_list_of_fields()

            previous = 'id'
            for field in list_of_fields:
                ordered_fields.append({
                    'Field': field,
                    'Previous': previous,
                })
                previous = field.field

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
            for ordered_field in ordered_fields:
                field = ordered_field['Field']
                previous = ordered_field['Previous']
                # stage column swap
                list_of_changes.append(MigrationProcessor.stage_swap_column(self._model, field, previous))

            self._staged_changes = list_of_changes

        @property
        def staged_changes(self):
            return self._staged_changes

    objects: _Objects
    checker: _Checker

    def __init__(self):
        self.objects = self._Objects(self)
        self.checker = self._Checker(self)

    def is_relevant(self):
        return self.checker.check_if_table_is_relevant()

    def add_data(self, data: list[DataObject], commit: bool = False):
        self.objects.insert_data(data=data, commit=commit)

    def get_list_of_fields(self) -> list[FieldData]:
        fields_list: list[FieldData]
        fields_list = []
        for field_name, field in self.fields.items():
            fields_list.append(FieldData(
                field_name,
                field.sql_data_type,
            ))
        return fields_list
