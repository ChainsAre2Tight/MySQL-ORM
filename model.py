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
            # connect to database
            # get all entries from a database
            # convert entries to objects
            # return list of objects

            # or

            # create a processor that connects to a database
            # processor must return a list of objects
            # this function only defines that processor must return ALL objects

    def __init__(self):
        self.objects = Model.Objects(self.fields)


class MyModel(Model):
    fields = {
        'field1': fields.TextField(50),
        'field2': fields.IntegerField,
    }
