from abc import ABC, abstractmethod
from internals.dataobject import DataObject


class AbstractConnection(ABC):

    def __init__(self, host: str, user: str, password: str):
        self._host = host
        self._user = user
        self._password = password
        self._connected_to_db = False
        self._connection = None

    @abstractmethod
    def connect(self):
        pass

    @property
    def connection(self):
        return self._connection

    @abstractmethod
    def close(self):
        pass

    @property
    def cursor(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    def is_connected_to_db(self):
        return self._connected_to_db

    def __str__(self):
        return f"""Connected to {self._host}
as user {self._user}
and password {self._password}"""

    @property
    @abstractmethod
    def information(self):
        return {
            'host': self._host,
            'user': self._user,
            'password': self._password,
            'is_connected': self._connected_to_db,
        }


class AbstractModel(ABC):
    fields: dict
    table_name: str
    objects: object
    _checker: object

    @abstractmethod
    def is_relevant(self) -> bool:
        pass

    @abstractmethod
    def add_data(self, data: list[DataObject], commit: bool = False):
        pass


class AbstractProcessor(ABC):
    connection: AbstractConnection
    model: AbstractModel
    _data: dict

    def __init__(self, m, con: AbstractConnection):
        self.model = m
        self.connection = con

    @property
    def data(self):
        return self._data


