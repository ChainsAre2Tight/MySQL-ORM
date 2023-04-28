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
    null: bool
    default: None

    def __init__(self, name, datatype, null, default):
        self.field = name
        self.datatype = datatype
        self.null = null
        self.default = default

    @staticmethod
    def from_dict(d):
        """Creates an object from a dictionary"""
        name = d['Field']
        datatype = d['Type']
        null = d['Null'] == 'True'
        default = d['Default']
        return FieldData(name, datatype, null, default)

    @property
    def information(self):
        return {
            'Field': self.field,
            'Type': self.datatype,
            'Null': self.null,
            'Default': self.default,
        }

    @property
    def representation(self):
        return f"""{self.field} {self.datatype}"""

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if (
                    self.field == other.field,
                    self.datatype == other.datatype) == (True, True):
                return True
            else:
                return False
        raise NotImplementedError('Cannot compare different data types')
