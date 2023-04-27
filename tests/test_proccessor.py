import unittest
from internals.connector import *
from internals.processor import GetDataProcessor, GetTableInfoProcessor
from models import MyModel, TestModel

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

    # def test_unfiltered(self):
    #     p = GetDataProcessor(
    #         m=MyModel,
    #         con=c,
    #         f=None
    #     )
    #     p.get_data()
    #
    #     self.assertEqual(p.json_data, [
    #         {
    #             'aga': "['1123', '3211322']",
    #             'id': 1
    #         },
    #         {
    #             'aga': '321',
    #             'id': 2
    #         }
    #     ])  # add assertion here


class TestGetTableInfoProcessor(unittest.TestCase):
    def test_get_column_data(self):
        m = MyModel()
        p = GetTableInfoProcessor(con=c, m=m)
        p.get_data()
        self.assertEqual(p.json_data, [
            {'Default': None,
             'Extra': 'auto_increment',
             'Field': 'id',
             'Key': 'PRI',
             'Null': 'NO',
             'Type': 'int'},
            {'Default': None,
             'Extra': '',
             'Field': 'aga',
             'Key': '',
             'Null': 'YES',
             'Type': 'text'}
        ])


class TestMyModel(unittest.TestCase):
    # def test_MyModel_all(self):
    #     mymodel = MyModel()
    #     self.assertEqual([i.data for i in mymodel.objects.all()],
    #                      [{'aga': "['1123', '3211322']", 'id': 1}, {'aga': '321', 'id': 2}])

    def test_MyModel_filtered(self):
        mymodel = MyModel()
        self.assertEqual([i.data for i in mymodel.objects.filter(
            {'id': 2}
        )],
                         [{'aga': '321', 'id': 2}])

    def test_CheckRelevancy1(self):
        mymodel = MyModel()
        res = mymodel.is_relevant()
        print(res)
        print(mymodel._checker.relevant_columns)
        print(mymodel._checker.irrelevant_columns)
        print()
        self.assertFalse(res)

    def test_CheckRelevancy2(self):
        mymodel = TestModel()
        res = mymodel.is_relevant()
        print()
        print(mymodel._checker.relevant_columns)
        print(mymodel._checker.irrelevant_columns)
        print()
        self.assertTrue(res)


if __name__ == '__main__':
    unittest.main()
