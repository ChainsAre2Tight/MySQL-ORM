from internals.interfaces import _Config


class Config(_Config):
    connection_data = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'test',
    }
