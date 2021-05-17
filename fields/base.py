import abc

class BaseField(abc.ABC):
    TYPE = None

    def __init__(self, *args, **kwargs):
        self._value = None
        self._raw_value = None
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self.validate(value)
        self._value = value

    @value.setter
    def raw_value(self, value):
        self._value = self.clean(value)
        self._raw_value = value

    @property
    def serialized_value(self):
        return self.value

    def serialize(self):
        return { self.TYPE: self.serialized_value }

    def validate(self, value):
        return

    def clean(self, value):
        self.validate(value)
        return value
