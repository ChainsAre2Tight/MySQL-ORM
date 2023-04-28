from internals.model import Model
from internals.database_fields import *


class MyModel(Model):
    table_name = 'test'
    fields = {
        'field1': TextField(null=False),
        'field2': IntegerField(),
    }


class TestModel(Model):
    table_name = 'test'
    fields = {
        'aga': TextField(null=False),
    }
