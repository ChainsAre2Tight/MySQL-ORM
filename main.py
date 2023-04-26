from connector import *
from proccesor import GetDataProcessor
from model import MyModel

c = DBConnection('localhost', 'root', 'root', 'test')
p = GetDataProcessor(
    m=MyModel,
    con=c,
    f={
        'aga': '321'
    },
)

p2 = GetDataProcessor(
    m=MyModel,
    con=c,
    f=None,
)

if __name__ == '__main__':
    p2.get_data()
    print(p2.data)
    print('\n'.join(p2.json_data))
