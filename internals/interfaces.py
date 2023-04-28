from abc import ABC, abstractmethod
from internals.dataobject import DataObject, FieldData


class _AbstractConnection(ABC):
    """Interface for connections"""
    _host: str
    _user: str
    _password: str
    _connected_to_db: bool
    _connection: object | None

    @abstractmethod
    def connect(self):
        """Creates a database connection and assigns it to connection attribute"""
        pass

    @property
    @abstractmethod
    def connection(self) -> object:
        """Returns a reference to connection that can be assigned via .connect()"""
        return self._connection

    @abstractmethod
    def close(self):
        """Closes connection"""
        pass

    @property
    @abstractmethod
    def cursor(self):
        """Returns a reference to a cursor() object"""
        pass

    @abstractmethod
    def commit(self):
        """Commits changes to the database"""
        pass

    @property
    def is_connected_to_db(self) -> bool:
        """Returns True if connected to a database, False if the connection is general"""
        return self._connected_to_db

    @property
    @abstractmethod
    def information(self) -> dict:
        """Returns data about the connection"""
        return {
            'host': self._host,
            'user': self._user,
            'password': self._password,
            'is_connected': self._connected_to_db,
        }


class _AbstractModel(ABC):
    """Interface for models"""
    fields: dict
    table_name: str
    objects: object
    checker: object

    class _Objects(ABC):
        """Interface for _Objects"""
        _fields: dict

        @abstractmethod
        def _get_data(self, f: dict | None) -> list[DataObject]:
            """
            Returns data from an assigned table
            :return: list of objects
            """
            pass

        @abstractmethod
        def all(self) -> list[DataObject]:
            """
            Returns all objects of this model
            :return: list of objects
            """
            pass

        @abstractmethod
        def filter(self, f: dict) -> list[DataObject]:
            """
            Returns objects of this model that match given filter
            :param f: filter {field_name: field_value}
            :return: list of objects
            """
            pass

        @abstractmethod
        def insert_data(self, data: list[DataObject], commit: bool):
            """
            Inserts data into a table, intended for internal use (forms)
            :param data: list of objects to insert
            :param commit: perform actual commits or not
            """
            pass

    class _Checker(ABC):
        """Interface for _Checker"""
        _fields: dict
        _staged_changes = list()

        @abstractmethod
        def _get_data(self) -> list[FieldData]:
            """
            Returns data from an assigned table
            :return: list of objects
            """
            pass

        @abstractmethod
        def get_changes(self) -> dict[str: list[dict]]:
            """
            Returns a dictionary that contains information about missing and odd columns of an assigned table
            :return: {'odd': [fields], 'missing': [fields]}
            """
            pass

        @abstractmethod
        def get_ordered_fields(self) -> list[dict[str: str]]:
            """
            Returns a list of dictionaries,
            each containing information about field's name, datatype and column that is before it
            :return: ({'Field': name, 'Type': datatype, 'Previous': name}, ...)
            """
            pass

        @abstractmethod
        def check_if_table_is_relevant(self) -> bool:
            """
            Performs a check and returns
            True if there is no odd or missing columns in the assigned table, false otherwise
            """
            pass

        @abstractmethod
        def stage_changes(self):
            """Stages changes for future execution, stores them in _staged_changes attribute"""
            pass

        @property
        def staged_changes(self) -> list:
            """Returns list of all staged changes"""
            return self._staged_changes

    objects: _Objects
    checker: _Checker

    @abstractmethod
    def is_relevant(self) -> bool:
        """
        Calls for checker.check_if_table_is_relevant
        :return: True, if table matches the model, False otherwise
        """
        pass

    @abstractmethod
    def add_data(self, data: list[DataObject], commit: bool = False):
        """
        Calls for objects.insert_data that inserts data into a table, intended for internal use (forms)
        :param data: list of objects to insert
        :param commit: perform actual commits or not
        """
        pass

    @abstractmethod
    def get_list_of_fields(self) -> list[FieldData]:
        """
        Converts Field objects into FieldData objects for further evaluation
        :return: list of FieldData objects
        """
        pass


class _AbstractProcessor(ABC):
    """Interface for processors"""
    connection: _AbstractConnection
    model: _AbstractModel
    _data: list

    def __init__(self, m, con: _AbstractConnection):
        self.model = m
        self.connection = con

    @property
    def data(self):
        """Returns data from the processor"""
        return self._data


class Config(ABC):
    """Interface for configuration"""
    connection_data: dict


class _AbstractMigrator(ABC):
    migrations: list

    @abstractmethod
    def make_migrations(self, list_of_models: list[_AbstractModel]):
        """
        Stages migrations for all given models, see Model._Checker.stage_migrations for more info
        :param list_of_models: list of all models to stage changes for
        """
        pass

    @abstractmethod
    def migrate(self):
        pass
