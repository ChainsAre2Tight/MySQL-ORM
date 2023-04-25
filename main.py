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

if __name__ == '__main__':
    p.get_data()
