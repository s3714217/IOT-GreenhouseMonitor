import logging
from datetime import datetime
from notifications.pushbullet import Pushbullet

'''
Handles sending notifications and determining if notifications need to be sent
'''
class Notification:

    def __init__(self, sensor_data_repository, pushbullet_token = None):
        self.__repository = sensor_data_repository
        if pushbullet_token is not None:
            self.__pushbullet = Pushbullet(pushbullet_token)

    '''
    Determines if a notification has been sent for the specified device today
    '''
    def previously_sent(self, device = None):
        if self.__pushbullet is None:
            logging.error("Add pushbullet_token entry in config.json")

        date = datetime.now()
        # Haven't sent a notification yet
        return self.__repository.count_notifications_sent(date, device) != 0

    '''
    Will notify via pushbullet because a reading was out of the ranges supplied
    in the config
    '''
    def notify_outside_range(self, reasons):
        if self.__pushbullet is None:
            logging.error("Add pushbullet_token entry in config.json")
            return

        self.__pushbullet.send_note("Sensor Monitor", 
            "Out of range reading! %s" % ", ".join(reasons))
        self.__repository.insert_notification_log()

    '''
    Notify when a connected device is nearby
    '''
    def notify_connected_device(self, device, sensor_log, reasons):
        if self.__pushbullet is None:
            logging.error("Add pushbullet_token entry in config.json")
            return

        temperature = sensor_log.get_temperature()
        humidity = sensor_log.get_humidity()

        if len(reasons) is 0:    
            self.__pushbullet.send_note("Connected Device: %s" % device, 
                "Temp: %d, Humidity: %d, Status: OK" \
                % (temperature, humidity))
        else:
            self.__pushbullet.send_note("Connected Device: %s" % device, 
                "Temp: %d, Humidity: %d, Status: BAD %s" \
                % (temperature, humidity, ", ".join(reasons)))
        self.__repository.insert_notification_log(device)