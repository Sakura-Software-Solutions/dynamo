import datetime as dt
from fields.base import BaseField

class Date(BaseField):
    TYPE = 'S'

    def dump(self):
        if not self.value:
            return None

        return { self.TYPE: self.value.isoformat() }

    def load(self, value):
        loaded_value = dt.datetime.fromisoformat(value).date()
        self.validate(loaded_value)
        self._value = loaded_value

    def validate(self, value):
        if type(value) is not(dt.date):
            raise ValueError("Value must be date.")


class DateTime(BaseField):
    TYPE = 'S'

    def dump(self):
        if not self.value:
            return None

        return { self.TYPE: self.value.isoformat() }

    def load(self, value):
        loaded_value = dt.datetime.fromisoformat(loaded_value)
        self.validate(loaded_value)
        self._value = loaded_value

    def validate(self, value):
        if type(value) is not(dt.datetime):
            raise ValueError("Value must be datetime.")
