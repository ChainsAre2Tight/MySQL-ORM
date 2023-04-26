import unittest
from connector import *
from proccesor import GetDataProcessor
from model import MyModel

c = DBConnection('localhost', 'root', 'root', 'test')


class TestGetDataProcessor(unittest.TestCase):

    def test_filtered(self):
        p = GetDataProcessor(
            m=MyModel,
            con=c,
            f={
                'aga': '321'
            },
        )
        p.get_data()

        self.assertEqual(p.json_data, [{'id': 2, 'aga': '321'}])  # add assertion here

    def test_unfiltered(self):
        p = GetDataProcessor(
            m=MyModel,
            con=c,
            f=None
        )
        p.get_data()

        self.assertEqual(p.json_data, [
            {
                'aga': "['1123', '3211322']",
                'id': 1
            },
            {
                'aga': '321',
                'id': 2
            }
        ])  # add assertion here


class TestMyModel(unittest.TestCase):
    def test_MyModel_all(self):
        mymodel = MyModel()
        self.assertEqual([i.data for i in mymodel.objects.all()],
                         [{'aga': "['1123', '3211322']", 'id': 1}, {'aga': '321', 'id': 2}])

    def test_MyModel_filtered(self):
        mymodel = MyModel()
        self.assertEqual([i.data for i in mymodel.objects.filter(
            {'id': 2}
        )],
                         [{'aga': '321', 'id': 2}])


if __name__ == '__main__':
    unittest.main()
