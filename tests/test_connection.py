import unittest
from internals.connector import TemplateConnection, DBConnection

configuration = ('localhost', 'root', 'root')


class ConnectionTest(unittest.TestCase):
    def test_connection(self):
        connection = TemplateConnection('localhost', 'root', 'root')
        self.assertEqual(
            connection.information,
            {
                'host': 'localhost',
                'user': 'root',
                'password': 'root',
                'is_connected': False
            }
        )

    def test_database_connection(self):
        connection = DBConnection('localhost', 'root', 'root', 'test')
        self.assertEqual(
            connection.information,
            {
                'host': 'localhost',
                'user': 'root',
                'password': 'root',
                'is_connected': True,
                'dbname': 'test'
            }
        )


if __name__ == '__main__':
    unittest.main()
