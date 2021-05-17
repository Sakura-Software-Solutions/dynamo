from fields.base import BaseField

class Integer(BaseField):
    TYPE = 'N'

    @property
    def serialized_value(self):
        return str(self.value)

    def validate(self, value):
        if type(value) is not(int):
            raise ValueError("Value must be integer.")


class Float(BaseField):
    TYPE = 'N'

    @property
    def serialized_value(self):
        return str(self.value)

    def validate(self, value):
        if type(value) is not(float):
            raise ValueError("Value must be float.")