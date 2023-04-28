from internals.connector import DBConnection
from internals.interfaces import _AbstractProcessor
from internals.dataobject import DataObject, FieldData
from config import Config


class _GetProcessor(_AbstractProcessor):
    pass


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

    @property
    def json_data(self) -> list[dict]:
        json_list = list()
        for obj in self._data:
            json_list.append(obj.data)
        return json_list


class GetTableInfoProcessor(_GetProcessor):
    _data = list[FieldData]

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
            list_of_objects.append(FieldData.from_dict(row))
        self._data = list_of_objects

    @property
    def json_data(self) -> list[dict]:
        json_list = list()
        for obj in self._data:
            json_list.append(obj.information)
        return json_list


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


class _AlterTableProcessor(_AbstractProcessor):
    _sql: str

    def generate_sql(self, field: FieldData):
        sql = ''
        self._sql = sql

    def perform(self, debug=False):

        if not debug:
            self.connection.connect()
            cursor = self.connection.cursor
            cursor.execute(self._sql)

            self.connection.commit()
            self.connection.close()
        else:
            print(self._sql)


class AddColumnProcessor(_AlterTableProcessor):
    def generate_sql(self, field: FieldData):
        sql = f"ALTER TABLE {self.model.table_name} ADD {field.representation};"
        self._sql = sql


class RemoveColumnProcessor(_AlterTableProcessor):
    def generate_sql(self, field: FieldData):
        sql = f"ALTER TABLE {self.model.table_name} DROP COLUMN {field.field};"
        self._sql = sql


class SwapColumnsProcessor(_AlterTableProcessor):
    def generate_sql(self, field: FieldData, previous: str):
        sql = f"""ALTER TABLE {self.model.table_name}
MODIFY COLUMN {field.representation} AFTER {previous};"""
        self._sql = sql


class AlterDefaultValueProcessor(_AlterTableProcessor):
    def generate_sql(self, field: FieldData):
        sql = f"""ALTER TABLE {self.model.table_name} ALTER COLUMN {field.field} {
        'SET DEFAULT ' + field.default if field.default is not None else 'DROP DEFAULT'}"""
        self._sql = sql


class AlterNullableProcessor(_AlterTableProcessor):
    def generate_sql(self, field: FieldData):
        sql = f"""ALTER TABLE {self.model.table_name} ALTER COLUMN {field.representation} {
        'NULL' if field.null else 'NOT NULL'}"""
        self._sql = sql


class MigrationProcessor:
    @staticmethod
    def stage_add_column(model, field):
        def perform_add_column(debug=False):
            connection = DBConnection(**Config.connection_data)
            processor = AddColumnProcessor(model, connection)
            processor.generate_sql(field)
            processor.perform(debug=debug)

        return perform_add_column

    @staticmethod
    def stage_remove_column(model, field):
        def perform_delete_column(debug=False):
            connection = DBConnection(**Config.connection_data)
            processor = RemoveColumnProcessor(model, connection)
            processor.generate_sql(field)
            processor.perform(debug=debug)

        return perform_delete_column

    @staticmethod
    def stage_swap_column(model, field, prev):
        def perform_swap_columns(debug=False):
            connection = DBConnection(**Config.connection_data)
            processor = SwapColumnsProcessor(model, connection)
            processor.generate_sql(field, previous=prev)
            processor.perform(debug=debug)

        return perform_swap_columns

    @staticmethod
    def stage_alter_default_value(model, field):
        def perform_alter_default_value(debug=False):
            connection = DBConnection(**Config.connection_data)
            processor = AlterDefaultValueProcessor(model, connection)
            processor.generate_sql(field)
            processor.perform(debug=debug)

        return perform_alter_default_value

    @staticmethod
    def stage_alter_nullable(model, field):
        def perform_alter_nullable(debug=False):
            connection = DBConnection(**Config.connection_data)
            processor = AlterNullableProcessor(model, connection)
            processor.generate_sql(field)
            processor.perform(debug=debug)

        return perform_alter_nullable
