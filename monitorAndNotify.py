import os
from data.sensor_data_sqlite_repository import SensorDataSqliteRepository
from data.database_initialiser import DatabaseInitialiser
from virtual_sense_hat import VirtualSenseHat

class MonitorAndNotify:

    def __init__(self):
        DatabaseInitialiser().init_sensor_data()
        self.__sensor_data_repository = SensorDataSqliteRepository()

    def monitor_sensor_data(self):
        # Get readings from SenseHat
        sense = VirtualSenseHat.getSenseHat()
        temperature = sense.get_temperature()
        humidity = sense.get_humidity()
        # Store in database
        self.__sensor_data_repository.insert_sensor_log(temperature, humidity)
        # TODO: Send PushBullet notification if outside range and would not have sent already

MonitorAndNotify().monitor_sensor_data()