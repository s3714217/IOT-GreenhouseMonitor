#!/usr/bin/env python3
import bluetooth
import logging
import os
import subprocess as sp
from config import Config
from data.database_initialiser import DatabaseInitialiser
from data.sensor_data_sqlite_repository import SensorDataSqliteRepository
from helpers.readings_validator import ReadingsValidator
from monitorAndNotify import MonitorAndNotify
from notifications.notification import Notification

class GreenhouseBluetooth:

    def __init__(self, sensor_data_repository, pushbullet_token):
        self.__notification = None if pushbullet_token is None else \
            Notification(sensor_data_repository, pushbullet_token)

    '''
    Get a list of all paired devices MAC addresses
    '''
    def get_paired_bluetooth_devices(self):
        p = sp.Popen(["sudo", "bt-device", "--list"], stdin = sp.PIPE, stdout = sp.PIPE, close_fds = True)
        (stdout, stdin) = (p.stdout, p.stdin)
        data = stdout.readlines()
        # Parse all devices
        devices = []
        for i in range(1, len(data)):
            entry = data[i].decode()
            start = entry.rfind("(")
            end = entry.rfind(")")
            devices.append(entry[start+1:end])
        return devices

    '''
    Notify any connected (paired) devices
    '''
    def notify_if_required(self, paired_devices, sensor_log, reasons):
        # Cross reference nearby devices to paired devices
        nearby_devices = bluetooth.discover_devices()
        currently_connected_device = []
        for device in nearby_devices:
            if device in paired_devices:
                currently_connected_device.append(device)
        # Notify each new nearby device
        if (len(currently_connected_device) > 0):
            logging.debug("Connected device found")
            for device in currently_connected_device:
                previously_sent = self.__notification.previously_sent(device)
                if previously_sent is False:
                    logging.debug("Connected device notification required")
                    self.__notification.notify_connected_device(
                        device, sensor_log, reasons)
                else:
                    logging.debug("Connected device notification already sent")
        else:
            logging.debug("Connected device notification not required")

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

    # Check for connected bluetooth devices
    bt = GreenhouseBluetooth(repository, pushbullet_token)
    paired_devices = bt.get_paired_bluetooth_devices()

    # Notify
    monitor = MonitorAndNotify(repository, readings_validator)
    sensor_log = monitor.monitor_sensor_data()
    bt.notify_if_required(paired_devices, sensor_log, \
        readings_validator.validate_sensor_log(sensor_log))