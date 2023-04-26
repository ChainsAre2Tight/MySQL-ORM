class DataObject:
    _data: tuple

    def __init__(self, d):
        self._data = d

    @staticmethod
    def from_dict(d):
        return DataObject(d)

    @property
    def data(self):
        return self._data

    def __str__(self) -> str:
        return str(self._data)
