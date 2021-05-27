import boto3
from client import exceptions

_client = None

class DynamoClient(object):
    exceptions = exceptions

    def __init__(self):
        self.client = boto3.client('dynamodb')

    def describe_table(self, table_name):
        try:
            return self.client.describe_table(TableName=table_name)

        except self.client.exceptions.ResourceNotFoundException:
            raise exceptions.TableNotFound(table_name)

    def create_table(self, table_name, attribute_definitions, key_schema):
        return self.client.create_table(
            TableName=table_name,
            AttributeDefinitions=attribute_definitions,
            KeySchema=key_schema,
            BillingMode='PAY_PER_REQUEST',
        )

    def get_item(self, table_name, key):
        try:
            response = self.client.get_item(TableName=table_name, Key=key)

            if 'Item' not in response:
                raise exceptions.ItemNotFound(table_name, key)

            return _parse_item(response['Item'])

        except self.client.exceptions.ResourceNotFoundException:
            raise exceptions.TableNotFound(table_name)

    def put_item(self, table_name, item):
        try:
            return self.client.put_item(TableName=table_name, Item=item)

        except self.client.exceptions.ResourceNotFoundException:
            raise exceptions.TableNotFound(table_name)
            
    @staticmethod
    def get_client():
        global _client

        if _client is None:
            _client = DynamoClient()

        return _client


def _parse_item_list(items):
    parsed_item_list = list()

    for item in items:
        value = list(item.values())[0]
        value = _parse_item(value)
        parsed_item_list.append(value)

    return parsed_item_list


def _parse_item(item):
    parsed_item = dict()

    for key, value in item.items():
        value = list(value.values())[0]

        if type(value) is dict:
            value = _parse_item(value)

        if type(value) is list:
            value = _parse_item_list(value)

        parsed_item[key] = value

    return parsed_item