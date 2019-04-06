import os
import sqlite3

class DatabaseInitialiser():

    CREATE_SENSOR_LOG_SQL = "CREATE TABLE `SensorLog` ( \
            `Id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, \
            `Temperature` INTEGER NOT NULL, \
            `Humidity` INTEGER NOT NULL, \
            `Timestamp` DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')) \
        );"

    CREATE_NOTIFICATION_LOG_SQL = "CREATE TABLE `NotificationLog` ( \
            `Timestamp` DATETIME PRIMARY KEY UNIQUE DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')), \
            `Device` TEXT DEFAULT NULL  \
        );"

    def __init__(self):
        pass

    '''
    Determine if a database exists
    '''
    def database_exists(self, database_name):
        database = "%s/resources/%s.db" % (os.getcwd(), database_name)
        return os.path.isfile(database)

    '''
    Create a table within a database
    '''
    def create_table(self, database_name, sql):
        root_directory = "%s/resources" % os.getcwd()
        if not os.path.exists(root_directory):
            os.mkdir(root_directory)
        database = "%s/%s.db" % (root_directory, database_name)
        with sqlite3.connect(database) as connection:
            connection.execute(sql)
    
    '''
    Initialise the sensor_data database
    '''
    def init_sensor_data(self):
        database_name = "sensor_data"
        if not self.database_exists(database_name):
            self.create_table(database_name, self.CREATE_SENSOR_LOG_SQL)
            self.create_table(database_name, self.CREATE_NOTIFICATION_LOG_SQL)