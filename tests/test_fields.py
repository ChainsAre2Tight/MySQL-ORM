import unittest


class lox:
    def __init__(self, a):
        self._a = a

    def __str__(self):
        return f'{self._a}'


class MyTestCase(unittest.TestCase):
    def test_something(self):
        a = lox(123)
        b = lox(456)
        asd = {'1': a, '2': b}
        print(f'{[str(asd[i]) for i in asd.keys()]}')


if __name__ == '__main__':
    unittest.main()
