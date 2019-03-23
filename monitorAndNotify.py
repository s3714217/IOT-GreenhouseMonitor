import os
from data.sensor_data_sqlite_repository import SensorDataSqliteRepository
from data.database_initialiser import DatabaseInitialiser

class MonitorAndNotify:

    def __init__(self):
        DatabaseInitialiser().init_sensor_data()
        self.__sensor_data_repository = SensorDataSqliteRepository()

    # def monitor_sensor_data():
    #     # TODO: Get SenseHat temperature
    #     # TODO: Get SenseHat humidity
    #     self.__sensor_data_repository.insert_sensor_log(temperature, humidity)
    #     # TODO: Log if values are outside range
    #     # TODO: Send PushBullet notification if outside range and has not been sent already

MonitorAndNotify()