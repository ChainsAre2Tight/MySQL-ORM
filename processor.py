from connector import DBConnection
from abc import ABC
from abstract_model import AbstractModel
from dataobject import DataObject


class _AbstractProcessor(ABC):
    connection: DBConnection
    model: AbstractModel
    _data: dict

    def __init__(self, m, con: DBConnection):
        self.model = m
        self.connection = con

    @property
    def data(self):
        return self._data

    @property
    def json_data(self):
        json_list = list()
        for obj in self._data:
            json_list.append(obj.data)
        return json_list


class GetDataProcessor(_AbstractProcessor):
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
            sql = f"SELECT * FROM {self.model.table_name} WHERE {self.filter_to_string}"
        else:
            sql = f"SELECT * FROM {self.model.table_name}"

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


class GetTableInfoProcessor(_AbstractProcessor):
    _data = dict

    def get_data(self):
        # generate SQL query
        sql = f'SHOW COLUMNS FROM {self.model.table_name}'
        # create a processor that retrieves column data from a database
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


