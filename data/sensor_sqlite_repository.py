import os
from data.sqlite_repository import SqliteRepository

'''
SQLite repository to handle persisting sensor data
'''
class SensorSqliteRepository(SqliteRepository):

    def __init__(self):
        database = os.getcwd()+"/resources/sensor_data.db"
        super().__init__(database)

    '''
    Insert an entry into the SensorLog table
    '''
    def insert_sensor_log(self, temperature, humidity):
        table = "SensorLog"
        items = {
            "TEMPERATURE": temperature,
            "HUMIDITY": humidity
        }
        super().insert(table, items)