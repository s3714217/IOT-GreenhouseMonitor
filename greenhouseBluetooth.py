#!/usr/bin/env python3
import logging
import os
import subprocess as sp
from config import Config
from notifications.notification import Notification

class GreenhouseBluetooth:

    def __init__(self, sensor_data_repository, pushbullet_token):
        self.__notification = None if pushbullet_token is None else \
            Notification(sensor_data_repository, pushbullet_token)

    def get_paired_bluetooth_devices(self):
        p = sp.Popen(["bt-device","--list"], stding = sp.PIPE, stdout = sp.PIPE, close-fds = True) 
        (stdout, stdin) = (p.stdout, p.stdin) 
        data = stdout.readlines()
        logging.debug(data)
        str2 = []

      for str1 in data:
        if (str1 != data[0]):
          str1 = str1.split()
          str2.append(str1[len(str1)-1])
        else:
            pass
     #the MAC_address is still encoded with b'( )
        return str2

    def notify_if_required(self, paired_devices):
        device_MAC_address = None
        nearby_devices = bluetooth.discover_devices()
        currently_connected_device = []
      for str1 in paired_devices:
       for mac in nearby_devices:
           if (str1 == mac.encoded()):#the above mac_address is still encoded so I encoded the nearby address to comparing
              currently_connected_device.append(mac)#Identified connected device
            else:  # TODO: Send notification to devices we have not yet sent a notification to today
        pass

if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG)

    # Initialise database
    DatabaseInitialiser().init_sensor_data()

    # Instantiate dependencies
    config = Config()
    sensor_config = config.get_sensor_config()
    pushbullet_token = config.get_pushbullet_token()
    repository = SensorDataSqliteRepository(sensor_config)

    # Check for connected bluetooth devices and notify
    bluetooth = GreenhouseBluetooth(repository, pushbullet_token)
    paired_devices = bluetooth.get_paired_bluetooth_devices()
    bluetooth.notify_if_required(paired_devices)