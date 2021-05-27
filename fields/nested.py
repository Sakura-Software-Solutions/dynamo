from fields.base import BaseField

class NestedDocument(BaseField):
    TYPE = 'M'

    def __init__(self, mapped_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mapped_class = mapped_class

    def dump(self):
        if not self.value:
            return None

        return { self.TYPE: self.value.dump() }

    def load(self, value):
        loaded_value = self._mapped_class.load(value)
        self.validate(loaded_value)
        self._value = loaded_value

    def validate(self, value):
        if type(value) is not(self._mapped_class):
            message = "Value must be {}.".format(self._mapped_class.__name__)
            raise ValueError(message)


class List(BaseField):
    TYPE = 'L'
    LIST_TYPE = None

    def __init__(self, list_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.LIST_TYPE = list_class.TYPE
        self._list_class = list_class
        self._value = list()
        
    def dump(self):
        return { self.TYPE: [{ self.LIST_TYPE: v.dump() } for v in self.value] }

    def load(self, values):
        loaded_values = list()

        for value in values:
            loaded_value = self._list_class.load(value)
            loaded_values.append(loaded_value)

        self.validate(loaded_values)
        self._value = loaded_values

    def append(self, item):
        self._value.append(item)

    def validate(self, values):
        if not all(type(value) is self._list_class for value in values):
            message = "Value must be {}.".format(self._mapped_class.__name__)
            raise ValueError(message)

