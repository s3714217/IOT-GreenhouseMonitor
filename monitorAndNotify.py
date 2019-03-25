import logging
import os
from datetime import datetime
from config import Config
from data.sensor_data_sqlite_repository import SensorDataSqliteRepository
from data.database_initialiser import DatabaseInitialiser
from virtual_sense_hat import VirtualSenseHat

class MonitorAndNotify:

    def __init__(self, sensor_data_repository):
        self.__repository = sensor_data_repository

    '''
    Logs the current readings into the database and notifies via pushbullet if
    a reading is out of the ranges supplied in the config
    '''
    def monitor_sensor_data(self):
        # Get readings from SenseHat
        sense = VirtualSenseHat.getSenseHat()
        temperature = sense.get_temperature()
        humidity = sense.get_humidity()
        # Store in database
        self.__repository.insert_sensor_log(temperature, humidity)

    '''
    Sends a notification if outside the ranges supplied in the config
    '''
    def notify_if_required(self):
        notify = self.notification_required()
        if notify is True:
            logging.info("Notification required")
            self.notify_outside_range()
        else:
            logging.info("Notification not required")

    '''
    Determines if the reading was outside the ranges supplied in the config
    '''
    def notification_required(self):
        count = self.__repository.count_out_of_range_logs(datetime.now())
        return count == 1

    '''
    Will notify via pushbullet because a reading was out of the ranges supplied
    in the config. This will only occur once per day
    '''
    def notify_outside_range(self):
        pass # TODO: Send PushBullet notification

if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG)

    # Initialise database
    DatabaseInitialiser().init_sensor_data()

    # Instantiate dependencies
    config = Config()
    repository = SensorDataSqliteRepository(config.get_sensor_config())

    # Log sensor data and notify if required!
    monitor = MonitorAndNotify(repository)
    monitor.monitor_sensor_data()
    monitor.notify_if_required()