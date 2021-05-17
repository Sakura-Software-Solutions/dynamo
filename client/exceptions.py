
class TableNotFound(Exception):

    def __init__(self, table_name):
        self.table_name = table_name

    def __str__(self):
        return 'Table Not Found: {}'.format(self.table_name)
