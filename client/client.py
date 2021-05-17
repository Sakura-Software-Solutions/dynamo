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