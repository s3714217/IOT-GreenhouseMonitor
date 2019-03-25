import json
import os
from models.sensor_config import SensorConfig

class Config:

    def __init__(self):
        # Read config file
        with open(os.getcwd()+"/config.json", "r") as config_file:
            # Create required model classes
            config = json.load(config_file)
            self.__sensor_config = SensorConfig(
                config["min_temperature"], 
                config["max_temperature"],
                config["min_humidity"],
                config["max_humidity"])

    def get_sensor_config(self):
        return self.__sensor_config