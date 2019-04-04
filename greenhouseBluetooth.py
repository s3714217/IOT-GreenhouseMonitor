import logging
from config import Config
from pushbullet.pushbullet import PushBullet

class GreenhouseBluetooth:

    def __init__(self, pushbullet):
        self.__pushbullet = pushbullet

    def get_paired_bluetooth_devices(self):
        # TODO: Get list of paired devices MAC addresses
        # 1. Decode list output
        # 2. Parse each MAC entry by:
        # get index of last )
        # get index of last (
        # Substring whats in between those indexes
        return []

    def notify_if_required(self, paired_devices):
        # TODO: Determine which paired devices are currently connected
        # TODO: Send notification to devices we have not yet sent a notification to today
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