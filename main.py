from models import TestModel
from internals.dataobject import DataObject

if __name__ == '__main__':
    my_model = TestModel()

    d1 = DataObject.from_dict({
        'aga': 'test_insert_1',
    })

    d2 = DataObject.from_dict({
        'aga': 'test_insert_2',
    })

    my_model.add_data([d1, d2], commit=False)
