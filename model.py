from abc import ABC
import fields


class Model(ABC):
    fields: dict
    objects: object

    class Objects:
        def __init__(self, f):
            self._fields = f

        def all(self) -> tuple:
            raise NotImplementedError
            # create a processor that connects to a database
            # processor must return a list of objects
            # this function only defines that processor must return ALL objects

    def __init__(self):
        self.objects = Model.Objects(self.fields)

    def __str__(self):
        return f'{self.__class__} with fields {[str(self.fields[f]) for f in self.fields.keys()]}'


class MyModel(Model):
    fields = {
        'field1': fields.TextField(max_length=50),
        'field2': fields.IntegerField(),
    }
