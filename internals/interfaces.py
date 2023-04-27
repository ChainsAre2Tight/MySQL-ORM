from abc import ABC, abstractmethod
from internals.dataobject import DataObject


class _AbstractConnection(ABC):
    _host: str
    _user: str
    _password: str
    _connected_to_db: bool
    _connection: object | None

    @abstractmethod
    def connect(self):
        pass

    @property
    @abstractmethod
    def connection(self):
        return self._connection

    @abstractmethod
    def close(self):
        pass

    @property
    @abstractmethod
    def cursor(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @property
    def is_connected_to_db(self):
        return self._connected_to_db

    @property
    @abstractmethod
    def information(self):
        return {
            'host': self._host,
            'user': self._user,
            'password': self._password,
            'is_connected': self._connected_to_db,
        }


class _AbstractModel(ABC):
    fields: dict
    table_name: str
    objects: object
    checker: object

    class _Objects(ABC):
        _fields: dict

        @abstractmethod
        def _get_data(self, f: dict | None) -> list:
            pass

        @abstractmethod
        def all(self) -> list[DataObject]:
            pass

        @abstractmethod
        def filter(self, f: dict) -> list[DataObject]:
            pass

        @abstractmethod
        def insert_data(self, data: list[DataObject], commit: bool):
            pass

    class _Checker(ABC):
        _fields: dict
        _staged_changes = list()

        @abstractmethod
        def _get_data(self) -> list:
            pass

        @abstractmethod
        def get_changes(self) -> dict[str: list[dict]]:
            pass

        @abstractmethod
        def get_ordered_fields(self) -> list[dict[str: str]]:
            pass

        @abstractmethod
        def check_if_table_is_relevant(self) -> bool:
            pass

        @abstractmethod
        def stage_changes(self):
            pass

        @property
        def staged_changes(self):
            return self._staged_changes

    objects: _Objects
    checker: _Checker

    @abstractmethod
    def is_relevant(self) -> bool:
        pass

    @abstractmethod
    def add_data(self, data: list[DataObject], commit: bool = False):
        pass


class _AbstractProcessor(ABC):
    connection: _AbstractConnection
    model: _AbstractModel
    _data: list

    def __init__(self, m, con: _AbstractConnection):
        self.model = m
        self.connection = con

    @property
    def data(self):
        return self._data

class _Config(ABC):
    connection_data: dict


class _AbstractMigrator(ABC):
    migrations: list

    @abstractmethod
    def make_migrations(self, list_of_models: list[_AbstractModel]):
        """
        Stages migrations for all given models
        :param list_of_models:
        """
        pass

    @abstractmethod
    def migrate(self):
        pass
