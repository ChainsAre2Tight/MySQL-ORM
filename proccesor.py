from connector import DBConnection
from model import Model
from abc import ABC


class AbstractProcessor(ABC):
    connection: DBConnection
    model: Model

    def __init__(self, m, con: DBConnection):
        self.model = m
        self.connection = con


class GetDataProcessor(AbstractProcessor):
    filter: dict
    _data: list

    def __init__(self, m, con: DBConnection, f: dict | None):
        super().__init__(m, con)
        self.filter = f

    @property
    def filter_to_string(self):
        list_filter = list()
        for key, value in self.filter.items():
            list_filter.append(f"{key} = {value}")
        return ' AND '.join(list_filter)

    def get_data(self):
        # generate SQL query
        if self.filter is not None:
            sql = f"SELECT * FROM {self.connection.dbname} WHERE {self.filter_to_string}"
        else:
            sql = f"SELECT * FROM {self.connection.dbname}"

        # connect to database
        self.connection.connect()
        cursor = self.connection.cursor

        # execute sql query
        cursor.execute(sql)
        data = cursor.fetchall()

        # close connection
        self.connection.close()

        list_of_objects = list()
        for row in data:
            list_of_objects.append(DataObject.from_dict(row))
        self._data = list_of_objects

    @property
    def data(self):
        return self._data

    @property
    def json_data(self):
        json_list = list()
        for obj in self._data:
            json_list.append(str(obj))
        return json_list


class DataObject:
    _data: tuple

    def __init__(self, d):
        self._data = d

    @staticmethod
    def from_dict(d):
        return DataObject(d)

    @property
    def data(self):
        return self._data

    def __str__(self) -> str:
        return str(self._data)
