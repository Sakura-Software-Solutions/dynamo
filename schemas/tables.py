import inflection
from client import DynamoClient
from schemas.base import BaseSchema


class Table(BaseSchema):
    __tablekeys__ = dict()
    _client = DynamoClient.get_client()
    
    @classmethod
    def table_name(cls):
        return inflection.underscore(cls.__name__)

    @classmethod
    def attribute_definitions(cls):
        attribute_definitions = list() 

        for field_name, key_type in cls.__tablekeys__.items():
            attribute_definition = dict(
                AttributeName=field_name, 
                AttributeType=getattr(cls, field_name).TYPE,
            )
            attribute_definitions.append(attribute_definition)

        return attribute_definitions

    @classmethod
    def key_schema(cls):
        key_schema = list()

        for field_name, key_type in cls.__tablekeys__.items(): 
            key = dict(
                AttributeName=field_name,
                KeyType=key_type,
            )
            key_schema.append(key)

        return key_schema

    @classmethod
    def create_table(cls):
        table_name = cls.table_name()
        key_schema = cls.key_schema()
        attribute_definitions = cls.attribute_definitions()

        return cls._client.create_table(table_name, attribute_definitions, key_schema)

    @classmethod
    def sync_table(cls):
        table_name = cls.table_name()

        try:
            description = cls._client.describe_table(table_name)

        except DynamoClient.exceptions.TableNotFound:
            cls.create_table()
            return True

        # TODO: If table already exists, make sure keys are in sync.
        else:
            return False

    @classmethod
    def get_item(cls, **kwargs):
        key = dict()

        for field_name, value in kwargs.items():
            field_type = getattr(cls, field_name).TYPE

            if field_type == 'N':
                value = str(value)

            key[field_name] = { field_type: value }

        item_dict = cls._client.get_item(cls.table_name(), key)

        return cls.load(item_dict)

    def save(self): 
        return self._client.put_item(self.table_name(), self.dump())
