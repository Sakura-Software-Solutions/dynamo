from fields.base import BaseField

class Integer(BaseField):
    TYPE = 'N'

    def dump(self):
        return { self.TYPE: str(self.value) }

    def load(self, value):
        loaded_value = int(value)
        self.validate(loaded_value)
        self._value = loaded_value

    def validate(self, value):
        if type(value) is not(int):
            raise ValueError("Value must be integer.")


class Float(BaseField):
    TYPE = 'N'

    def dump(self):
        return { self.TYPE: str(self.value) }

    def load(self, value):
        loaded_value = float(value)
        self.validate(loaded_value)
        self._value = loaded_value

    def validate(self, value):
        if type(value) is not(float):
            raise ValueError("Value must be float.")