import logging
from config import Config
from pushbullet.pushbullet import PushBullet
import subprocess as sp
import os

class GreenhouseBluetooth:

    def __init__(self, pushbullet):
        self.__pushbullet = pushbullet

    def get_paired_bluetooth_devices(self):
       p = sp.Popen(["bt-device","--list"], stding = sp.PIPE, stdout = sp.PIPE, close-fds = True) 
       (stdout, stdin) = (p.stdout, p.stdin) 
        data = stdout.readlines()
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

    # Instantiate dependencies
    config = Config()
    pushbullet_token = config.get_pushbullet_token()
    pushbullet = PushBullet(pushbullet_token)

    bluetooth = GreenhouseBluetooth(pushbullet)
    paired_devices = bluetooth.get_paired_bluetooth_devices()
    bluetooth.notify_if_required(paired_devices)
