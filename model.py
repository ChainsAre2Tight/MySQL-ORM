from abc import ABC
import database_fields
from proccesor import GetDataProcessor
from connector import DBConnection
from config import Config


class AbstractModel(ABC):
    fields: dict
    table_name: str


class Model(AbstractModel):
    class Objects:
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

        def all(self) -> tuple:
            return self._get_data(f=None)

        def filter(self, f: dict) -> tuple:
            return self._get_data(f=f)

    objects: Objects

    def __init__(self):
        self.objects = self.Objects(self)

    def __str__(self):
        return f'{self.__class__} with fields {[str(self.fields[f]) for f in self.fields.keys()]}'


class MyModel(Model):
    table_name = 'test'
    fields = {
        'field1': database_fields.TextField(max_length=50),
        'field2': database_fields.IntegerField(),
    }
