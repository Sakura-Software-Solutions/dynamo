from fields.base import BaseField

class NestedDocument(BaseField):
    TYPE = 'M'

    def __init__(self, mapped_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mapped_class = mapped_class

    @property
    def serialized_value(self):
        return self.value.serialize() if self.value else None

    def validate(self, value):
        if type(value) is not(self._mapped_class):
            message = "Value must be {}.".format(self._mapped_class.__name__)
            raise ValueError(message)


class List(BaseField):
    TYPE = 'L'
    LIST_TYPE = None

    def __init__(self, list_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.LIST_TYPE = list_class.TYPE if issubclass(list_class, BaseField) else 'M'
        self._list_class = list_class
        self._value = list()
        

    @property
    def serialized_value(self):
        return [{ self.LIST_TYPE: v.serialize() } for v in self.value]

    def append(self, item):
        self._value.append(item)

    def validate(self, value):
        if not all(type(v) is self._list_class for v in value):
            message = "Value must be {}.".format(self._mapped_class.__name__)
            raise ValueError(message)

