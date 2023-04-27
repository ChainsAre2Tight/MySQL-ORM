from internals.connector import DBConnection
from internals.interfaces import _AbstractProcessor
from internals.dataobject import DataObject


class _GetProcessor(_AbstractProcessor):
    @property
    def json_data(self):
        json_list = list()
        for obj in self._data:
            json_list.append(obj.data)
        return json_list


class GetDataProcessor(_GetProcessor):
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


class GetTableInfoProcessor(_GetProcessor):
    _data = list

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


class InsertDataProcessor(_AbstractProcessor):
    _data = list

    def __init__(self, m, con: DBConnection, d: list[DataObject]):
        super().__init__(m, con)
        self._data = d

    def generate_sql(self) -> tuple[str, list]:
        values_list: list[dict]
        sql: str

        data = list()
        values_list = list()
        for obj in self._data:
            row = obj.data
            values_list.append(row)
            data.append(list(row.values()))

        fields: list[str]
        fields = list(values_list[0].keys())
        fields_to_string = ', '.join(fields)

        data_to_string = ', '.join([f"({', '.join(row)})" for row in data])

        sql = f"""INSERT INTO {self.model.table_name} ({fields_to_string}) VALUES ({'%s' * len(fields)});"""
        return sql, data

    def insert_data(self, commit: bool):
        # generate SQL query
        sql, data = self.generate_sql()
        # create a processor that retrieves column data from a database
        self.connection.connect()
        cursor = self.connection.cursor

        # execute sql query
        for row in data:
            cursor.execute(sql, row)
        if commit:
            self.connection.commit()

        # close connection
        self.connection.close()
        pass
