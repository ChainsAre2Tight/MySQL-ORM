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


class FieldData:
    """Objects that is used for a common representation and evaluation of fields and columns """
    field: str
    datatype: str

    def __init__(self, name, datatype, *args, **kwargs):
        self.field = name
        self.datatype = datatype

    @staticmethod
    def from_dict(d):
        """Creates an object from a dictionary"""
        name = d['Field']
        datatype = d['Type']
        return FieldData(name, datatype)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.field == other.field and self.datatype == other.datatype:
                return True
            else:
                return False
        raise NotImplementedError('Cannot compare different data types')

    @property
    def information(self):
        return {
            'Field': self.field,
            'Type': self.datatype,
        }
