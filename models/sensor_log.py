from datetime import datetime

class SensorLog:

    def __init__(self, temperature, humidity, timestamp = datetime.now()):
        self.__temperature = temperature
        self.__humidity = humidity
        self.__timestamp = timestamp

    def get_temperature(self):
        return self.__temperature

    def get_humidity(self):
        return self.__humidity

    def get_timestamp(self):
        return self.__timestamp