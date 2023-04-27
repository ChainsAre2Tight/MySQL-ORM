import database_fields
from processor import GetDataProcessor, GetTableInfoProcessor, InsertDataProcessor
from connector import DBConnection
from config import Config
from abstract_model import AbstractModel
from dataobject import DataObject


class Model(AbstractModel):
    class _Objects:
        _fields: dict

        def __init__(self, m: AbstractModel):
            self._model = m
            self._fields = self._model.fields

        def _get_data(self, f: dict | None):
            # create a processor that connects to a database
            connection = DBConnection(**Config.connection_data)
            processor = GetDataProcessor(self._model, connection, f=f)
            processor.get_data()
            # processor must return a list of objects
            data = processor.data
            # this function only defines that processor must return ALL objects (f=None)
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
        relevant_columns: dict
        irrelevant_columns: dict

        def __init__(self, m: AbstractModel):
            self._model = m
            self._fields = self._model.fields

        def _get_data(self):
            # create a processor that connects to a database
            connection = DBConnection(**Config.connection_data)
            processor = GetTableInfoProcessor(self._model, connection)
            processor.get_data()
            # processor returns a list of objects
            data = processor.data
            # this function only defines that processor must return ALL objects (f=None)
            return data

        def get_relevant_and_irrelevant_columns(self):
            # retrieve data about columns from table
            data = self._get_data()

            self.relevant_columns = dict()
            self.irrelevant_columns = dict()
            # TODO make a column checker that actually works
            for field_name, field in self._model.fields.items():
                flag = False
                for column in data:
                    column_data = column.data
                    if column_data['Field'] == field_name and column_data['Type'] == field.sql_data_type:
                        flag = True
                if flag:
                    self.relevant_columns[field_name] = field
                else:
                    self.irrelevant_columns[field_name] = field

        def check_if_table_is_relevant(self) -> bool:
            self.get_relevant_and_irrelevant_columns()
            if len(self.irrelevant_columns) == 0 and len(self.relevant_columns) == len(self._model.fields.keys()):
                return True
            return False

    objects: _Objects
    _checker: _Checker

    def __init__(self):
        self.objects = self._Objects(self)
        self._checker = self._Checker(self)

    def is_relevant(self):
        return self._checker.check_if_table_is_relevant()

    def add_data(self, data: list[DataObject], commit: True):
        self.objects.insert_data(data=data, commit=commit)


class MyModel(Model):
    table_name = 'test'
    fields = {
        'field1': database_fields.TextField(),
        'field2': database_fields.IntegerField(),
        'aga': database_fields.TextField(),
    }


class TestModel(Model):
    table_name = 'test'
    fields = {
        'aga': database_fields.TextField(),
    }
