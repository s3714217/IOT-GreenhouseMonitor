import json
import logging
import os
from models.sensor_config import SensorConfig

'''
Parses the config.json
'''
class Config:

    def __init__(self):
        # Read config file and create required model classes
        with open(os.getcwd()+"/config.json", "r") as config_file:
            config = json.load(config_file)
            # Sensor config
            self.__sensor_config = SensorConfig(
                config["min_temperature"], 
                config["max_temperature"],
                config["min_humidity"],
                config["max_humidity"])
            # PushBullet config
            if "pushbullet_token" in config:
                logging.debug("Pushbullet token found")
                self.__pushbullet_token = config["pushbullet_token"]
            else:
                logging.error("Add pushbullet_token entry in config.json")
                self.__pushbullet_token = None

    def get_sensor_config(self):
        return self.__sensor_config

    def get_pushbullet_token(self):
        return self.__pushbullet_token