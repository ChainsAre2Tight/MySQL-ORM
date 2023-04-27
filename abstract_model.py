from abc import ABC, abstractmethod
from dataobject import DataObject


class AbstractModel(ABC):
    fields: dict
    table_name: str
    objects: object
    _checker: object

    @abstractmethod
    def is_relevant(self) -> bool:
        pass

    @abstractmethod
    def add_data(self, data: list[DataObject], commit: bool = False):
        pass
