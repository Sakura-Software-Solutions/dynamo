import abc
import copy
from fields.base import BaseField

class BaseSchema(abc.ABC):

    def __init__(self, *args, **kwargs):
        for field in self.fields():
            field_copy = copy.deepcopy(field['field'])
            super().__setattr__(field['name'], field_copy)

        for name, value in kwargs.items():
            super().__getattribute__(name).value = value

    def __getattribute__(self, name):
        attribute = super().__getattribute__(name)

        if issubclass(type(attribute), BaseField):
            attribute = attribute.value

        return attribute

    def __setattr__(self, name, value):
        try:
            attribute = super().__getattribute__(name)

        except AttributeError:
            super().__setattr__(name, value)

        else:
            if issubclass(type(attribute), BaseField):
                attribute.value = value
            else:
                super().__setattr__(name, value)

    def fields(self):
        fields = list()

        for name in dir(self):
            attribute = super().__getattribute__(name) 
        
            if issubclass(type(attribute), BaseField):
                field = dict(name=name, field=attribute)
                fields.append(field)

        return fields

    def serialize(self):
        dictionary = dict()

        for field in self.fields():
            name, attribute = field['name'], field['field']
            
            if attribute and (attribute.value is not None):
                dictionary[name] = attribute.serialize()

        return dictionary



