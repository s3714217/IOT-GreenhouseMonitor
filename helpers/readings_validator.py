class ReadingsValidator:

    def __init__(self, sensor_config):
        self.__config = sensor_config

    '''
    Validates the supplied sensor logs are within the configured ranges.
    Returns a list of reasons why it is not valid or an empty list if it is
    '''
    def validate_sensor_logs(self, sensor_logs):
        results = []
        # Return if there are no logs for the specified date
        if (len(sensor_logs) is 0):
            return results
        # Iterate over each log appending BAD results
        for log in sensor_logs:
            validity = self.validate_sensor_log(log)
            if (len(validity) is not 0):
                # Append each BAD reason to results
                for reason in validity:
                    results.append(reason)
        return results

    '''
    Validates the supplied sensor log is within the configured ranges.
    Returns a list of reasons why it is not valid or an empty list if it is
    '''
    def validate_sensor_log(self, sensor_log):
        # Validate each reading individually
        temp_validity = self.validate_temperature(sensor_log.get_temperature())
        hum_validity = self.validate_humidity(sensor_log.get_humidity())
        # Return results
        results = []
        if (temp_validity is not True):
            results.append(temp_validity)
        if (hum_validity is not True):
            results.append(hum_validity)
        return results

    '''
    Validates that the supplied temperature is within the configured ranges.
    Returns a list of reasons why it is not valid or True if it is
    '''
    def validate_temperature(self, temperature):
        # Get min max values
        min_temperature = self.__config.get_min_temperature()
        max_temperature = self.__config.get_max_temperature()
        # Validate
        if (temperature < min_temperature):
            return "%d *C below minimum temperature" % \
                (min_temperature - temperature)
        if (temperature > max_temperature):
            return "%d *C above maximum temperature" % \
                (temperature - max_temperature)
        # Must be OK
        return True

    '''
    Validates that the supplied humidity is within the configured ranges.
    Returns a list of reasons why it is not valid or True if it is
    '''
    def validate_humidity(self, humidity):
        # Get min max values
        min_humidity = self.__config.get_min_humidity()
        max_humidity = self.__config.get_max_humidity()
        # Validate
        if (humidity < min_humidity):
            return "%d%% below minimum humidity" % \
                (min_humidity - humidity)
        if (humidity > max_humidity):
            return "%d%% above maximum humidity" % \
                (humidity - max_humidity)
        # Must be OK
        return True