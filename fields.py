from abc import ABC, abstractmethod


class Field(ABC):
    _value: None
    _field_name: str

    def __init__(self, field_name, *args, **kwargs):
        self._field_name = field_name

    @property
    @abstractmethod
    def sql_data_type(self) -> str:
        raise NotImplementedError('calling an abstract method')

    @property
    def field_name(self) -> str:
        return self._field_name

    @property
    def sql_field(self) -> str:
        return f'{self.field_name} {self.sql_data_type}'


class TextField(Field):
    _value: str
    _max_length: int

    def __init__(self, field_name, max_length=255):
        super().__init__(self, field_name)
        self._max_length = max_length

    @property
    def sql_data_type(self) -> str:
        return f'VARCHAR({self._max_length})'


class IntegerField(Field):
    _value: int

    @property
    def sql_data_type(self) -> str:
        return f'INT'
