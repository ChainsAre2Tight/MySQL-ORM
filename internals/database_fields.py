from abc import ABC, abstractmethod


class Field(ABC):
    _value: None

    def __init__(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def sql_data_type(self) -> str:
        raise NotImplementedError('calling an abstract method')


class TextField(Field):
    _value: str
    _max_length: int

    def __init__(self, max_length=256):
        super().__init__(self)
        self._max_length = max_length

    @property
    def sql_data_type(self) -> str:
        if self._max_length != 256:
            return f'text({self._max_length})'
        else:
            return 'text'


class IntegerField(Field):
    _value: int

    @property
    def sql_data_type(self) -> str:
        return f'int'
