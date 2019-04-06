#!/usr/bin/env python3
import logging
from config import Config
from data.database_initialiser import DatabaseInitialiser
from data.sensor_data_sqlite_repository import SensorDataSqliteRepository
from helpers.readings_validator import ReadingsValidator
from models.sensor_log import SensorLog
from notifications.notification import Notification
from virtual_sense_hat import VirtualSenseHat

class MonitorAndNotify:

    def __init__(self, sensor_data_repository, readings_validator, pushbullet_token = None):
        self.__repository = sensor_data_repository
        self.__readings_validator = readings_validator
        self.__notification = None if pushbullet_token is None else \
            Notification(self.__repository, pushbullet_token)

    '''
    Logs the current readings into the database
    '''
    def monitor_sensor_data(self):
        # Get readings from SenseHat
        sense = VirtualSenseHat.getSenseHat()
        temperature = sense.get_temperature()
        humidity = sense.get_humidity()
        sensor_log = SensorLog(temperature, humidity)
        # Store in database
        self.__repository.insert_sensor_log(sensor_log)
        return sensor_log

    '''
    Sends a notification if outside the ranges supplied in the config
    '''
    def notify_if_required(self, sensor_log):
        if self.__notification is None:
            return

        # Validate readings were outside ranges
        results = self.__readings_validator.validate_sensor_log(sensor_log)
        if len(results) is 0:
            logging.info("Notification not required")
            return
        
        # Ensure a notification has not already been sent
        previously_sent = self.__notification.previously_sent()
        if previously_sent is False:
            logging.info("Notification required")
            self.__notification.notify_outside_range(results)
        else:
            logging.info("Notification not required")

if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG)

    # Initialise database
    DatabaseInitialiser().init_sensor_data()

    # Instantiate dependencies
    config = Config()
    sensor_config = config.get_sensor_config()
    pushbullet_token = config.get_pushbullet_token()
    repository = SensorDataSqliteRepository(sensor_config)
    readings_validator = ReadingsValidator(sensor_config)

    # Log sensor data and notify if required!
    monitor = MonitorAndNotify(repository, readings_validator, pushbullet_token)
    sensor_log = monitor.monitor_sensor_data()
    monitor.notify_if_required(sensor_log)