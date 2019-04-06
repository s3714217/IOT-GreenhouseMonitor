import logging
from datetime import datetime
from notifications.pushbullet import Pushbullet

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