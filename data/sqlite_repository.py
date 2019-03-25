import sqlite3

'''
Generic SQLite repository
'''
class SqliteRepository():

    SEPARATOR = ", "

    INSERT_SQL = "INSERT INTO %s (%s) VALUES (%s)"

    ONLY_DEFAULT_VALUES_INSERT_SQL = "INSERT INTO %s DEFAULT VALUES"

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
    Prone to SQL Injection - But we would realistically use some sort of ORM
    '''
    def insert(self, table, items):
        # Split out the dictionary into separate lists
        keys = []
        values = []
        if items is not None:
            for key, value in items.items():
                keys.append(key)
                values.append(str(value))
        # Join each list into single strings
        keys_joined = self.SEPARATOR.join(keys)
        values_joined = self.SEPARATOR.join(values)
        # Insert into database
        if (len(keys) > 0):
            return self.execute(self.INSERT_SQL % (table, keys_joined, values_joined))
        else:
            return self.execute(self.ONLY_DEFAULT_VALUES_INSERT_SQL % table)
        
