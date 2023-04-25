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

    def __init__(self, m, con: DBConnection, f: dict | None):
        super().__init__(m, con)
        self.filter = f

    @property
    def filter_to_string(self):
        list_filter = list()
        for key, value in self.filter.items():
            list_filter.append(f"{key} = {value}")
        return ' AND '.join(list_filter)

    def get_data(self) -> tuple:
        # generate SQL query
        sql = f"SELECT * FROM {self.connection.dbname} WHERE {self.filter_to_string}"

        self.connection.cursor.execute(sql)
        data = self.connection.cursor.fetchall()
        self.connection.close()

        list_of_objects = list()
        for row in data:
            print(row)


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
