from fields.base import BaseField

class String(BaseField):
    TYPE = 'S'

    def validate(self, value):
        if type(value) is not(str):
            raise ValueError("Value must be string.")
