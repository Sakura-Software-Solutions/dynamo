from fields.base import BaseField

class Boolean(BaseField):
    TYPE = 'B'

    def validate(self, value):
        if type(value) is not(bool):
            raise ValueError("Value must be boolean.")
