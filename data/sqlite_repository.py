import sqlite3

'''
Generic SQLite repository
'''
class SqliteRepository():

    seperator = ", "

    insert_sql = "INSERT INTO %s (%s) VALUES (%s)"

    def __init__(self, database):
        self.__database = database

    '''
    Executes the supplied SQL query
    '''
    def execute(self, sql, args = None):
        with sqlite3.connect(self.__database) as connection:
            if (args is not None):
                return connection.execute(sql, args)
            else:
                return connection.execute(sql)

    '''
    Insert an entry into specified table with supplied items dictionary
    '''
    def insert(self, table, items):
        # Split out the dictionary into separate lists
        keys = []
        values = []
        for key, value in items.items():
            keys.append(key)
            values.append(str(value))
        # Join each list into single strings
        keys_joined = self.seperator.join(keys)
        values_joined = self.seperator.join(values)
        # Insert into database
        return self.execute(self.insert_sql % (table, keys_joined, values_joined))