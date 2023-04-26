from abc import ABC


class AbstractModel(ABC):
    fields: dict
    table_name: str
    objects: object
