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

    def dump(self):
        return { self.TYPE: self.value }

    def load(self, value):
        self.validate(value)
        self._value = value

    def validate(self, value):
        return
