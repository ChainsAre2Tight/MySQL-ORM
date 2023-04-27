import unittest
from internals.migrator import Migrator
from models import TestModel, MyModel
from unittest import mock
import io


class TestMigration(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_nothing_to_change(self, mock_out):
        model = TestModel()
        migrator = Migrator()
        migrator.make_migrations([model])
        migrator.migrate(debug=True)
        self.assertEqual("""ALTER TABLE test
MODIFY COLUMN aga text AFTER id;
""", mock_out.getvalue())

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_everything_to_change(self, mock_out):
        model = MyModel()
        migrator = Migrator()
        migrator.make_migrations([model])
        migrator.migrate(debug=True)
        self.assertEqual("""ALTER TABLE test DROP COLUMN aga;
ALTER TABLE test ADD field1 text;
ALTER TABLE test ADD field2 int;
ALTER TABLE test
MODIFY COLUMN field1 text AFTER id;
ALTER TABLE test
MODIFY COLUMN field2 int AFTER field1;
""", mock_out.getvalue())




if __name__ == '__main__':
    unittest.main()
