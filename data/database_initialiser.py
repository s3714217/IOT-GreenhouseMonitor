import os
import sqlite3

class DatabaseInitialiser():

    create_sensor_data_sql = "CREATE TABLE `SensorLog` ( \
            `ID` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, \
            `TEMPERATURE` INTEGER NOT NULL, \
            `HUMIDITY` INTEGER NOT NULL, \
            `TIMESTAMP` DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'localtime')) \
        );"

    def __init__(self):
        pass

    def database_exists(self, database_name):
        database = "%s/resources/%s.db" % (os.getcwd(), database_name)
        return os.path.isfile(database)

    def create_table(self, database_name, sql):
        database = "%s/resources/%s.db" % (os.getcwd(), database_name)
        with sqlite3.connect(database) as connection:
            connection.execute(sql)
    
    def init_sensor_data(self):
        database_name = "sensor_data"
        if not self.database_exists(database_name):
            self.create_table(database_name, self.create_sensor_data_sql)