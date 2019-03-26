import logging
import os
from datetime import datetime
from config import Config
from data.sensor_data_sqlite_repository import SensorDataSqliteRepository
from data.database_initialiser import DatabaseInitialiser
from pushbullet.pushbullet import PushBullet
from virtual_sense_hat import VirtualSenseHat

class MonitorAndNotify:

    def __init__(self, sensor_data_repository, pushbullet_token = None):
        self.__repository = sensor_data_repository
        self.__pushbullet_token = pushbullet_token

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
        if self.__pushbullet_token is None:
            return

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
        date = datetime.now()
        if (self.__repository.count_notifications_sent(date) != 0):
            return False
        return self.__repository.count_out_of_range_logs(date) == 1

    '''
    Will notify via pushbullet because a reading was out of the ranges supplied
    in the config. This will only occur once per day
    '''
    def notify_outside_range(self):
        pushbullet = PushBullet(self.__pushbullet_token)
        pushbullet.send_note("Sensor Monitor", "Out of range reading!")
        self.__repository.insert_notification_log()

if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG)

    # Initialise database
    DatabaseInitialiser().init_sensor_data()

    # Instantiate dependencies
    config = Config()
    sensor_config = config.get_sensor_config()
    pushbullet_token = config.get_pushbullet_token()
    repository = SensorDataSqliteRepository(sensor_config)

    # Log sensor data and notify if required!
    monitor = MonitorAndNotify(repository, pushbullet_token)
    monitor.monitor_sensor_data()
    monitor.notify_if_required()