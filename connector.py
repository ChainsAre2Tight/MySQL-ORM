import pymysql.cursors
from abc import ABC, abstractmethod


class TemplateConnection(ABC):

    def __init__(self, host: str, user: str, password: str):
        self._host = host
        self._user = user
        self._password = password
        self._connected_to_db = False
        self._connection = pymysql.connect(
            host=self._host,
            user=self._user,
            password=self._password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
        )

    @property
    def connection(self):
        return self._connection

    def close(self):
        self._connection.close()

    @property
    def cursor(self):
        return self._connection.cursor()

    def commit(self):
        self._connection.commit()

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


class DBConnection(TemplateConnection):
    def __init__(self, host: str, user: str, password: str, dbname: str):
        super().__init__(host, user, password)
        self._connected_to_db = True
        self._dbname = dbname
        self._connection = pymysql.connect(
            host=self._host,
            user=self._user,
            password=self._password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            db=self._dbname
        )

    def __str__(self):
        return f"""Connected to {self._host}
        as user {self._user}
        and password {self._password}
        (database -> {self._dbname})"""

    @property
    def information(self):
        return {
            'host': self._host,
            'user': self._user,
            'password': self._password,
            'is_connected': self._connected_to_db,
            'dbname': self._dbname
        }

    @property
    def dbname(self):
        return self._dbname
