from internals.interfaces import Config


class Config(Config):
    connection_data = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'test',
    }
