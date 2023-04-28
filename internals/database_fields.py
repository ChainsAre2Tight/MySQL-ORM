from abc import ABC, abstractmethod


class Field(ABC):
    _value: None
    _can_be_null: bool
    _default: None

    def __init__(
            self,
            null: bool = True,
            default=None,
    ):
        self._can_be_null = null
        self._default = default

    @property
    @abstractmethod
    def sql_data_type(self) -> str:
        raise NotImplementedError('calling an abstract method')

    @property
    def null(self) -> bool:
        return self._can_be_null

    @property
    def default(self):
        return self._default


class TextField(Field):
    _value: str
    _max_length: int

    def __init__(
            self,
            null: bool = True,
            default: str | None = None,
            max_length: int = 256,
    ):
        super().__init__(
            null=null,
            default=default,
        )
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
