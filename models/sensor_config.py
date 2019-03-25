'''
Model class to store sensor configuration
'''
class SensorConfig:

    def __init__(self, min_temperature, max_temperature, min_humidity, max_humidity):
        self.__min_temperature = min_temperature
        self.__max_temperature = max_temperature
        self.__min_humidity = min_humidity
        self.__max_humidity = max_humidity

    def get_min_temperature(self):
        return self.__min_temperature
    
    def get_max_temperature(self):
        return self.__max_temperature

    def get_min_humidity(self):
        return self.__min_humidity
    
    def get_max_humidity(self):
        return self.__max_humidity