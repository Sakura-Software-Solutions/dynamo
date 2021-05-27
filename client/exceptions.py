
class TableNotFound(Exception):

    def __init__(self, table_name):
        self.table_name = table_name

    def __str__(self):
        return 'Table Not Found: {}'.format(self.table_name)


class ItemNotFound(Exception):
    def __init__(self, table_name, key):
        self.table_name = table_name
        self.key = key

    def __str__(self):
        return 'Item not found in table "{}"'.format(self.table_name)
