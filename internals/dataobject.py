class DataObject:
    _data: dict

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


class ColumnFieldData:
    datatype: str
    position: int

    def __init__(self, d, p):
        self.datatype = d
        self.position = p

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            if self.datatype == other.datatype and self.position == other.position:
                return True
            return False
        raise NotImplementedError('cannot compare instances of different classes')
