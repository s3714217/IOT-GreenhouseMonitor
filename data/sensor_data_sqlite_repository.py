import logging
import os
from datetime import datetime
from data.sqlite_repository import SqliteRepository
from models.sensor_log import SensorLog

'''
SQLite repository to handle persisting sensor data
'''
class SensorDataSqliteRepository(SqliteRepository):

    TEMPERATURE_INDEX = 0
    HUMIDITY_INDEX = 1
    TIMESTAMP_INDEX = 2
    DATE_FORMAT = "%Y-%m-%d"

    SELECT_DAYS_LOGS_SQL = "SELECT temperature, humidity, timestamp FROM SensorLog \
        WHERE timestamp >= DATE(:date) AND timestamp < DATE(:date, '+1 day')"

    COUNT_OUT_OF_RANGE_LOGS_SQL = "SELECT COUNT(*) FROM SensorLog \
        WHERE timestamp BETWEEN DATE(:date) AND DATE(:date, '+1 day') \
        AND (temperature NOT BETWEEN :min_temperature AND :max_temperature \
        OR humidity NOT BETWEEN :min_humidity AND :max_humidity)"

    def __init__(self, config):
        self.__config = config
        database = os.getcwd()+"/resources/sensor_data.db"
        super().__init__(database)

    '''
    Insert an entry into the SensorLog table
    '''
    def insert_sensor_log(self, temperature, humidity):
        logging.debug("Inserting SensorLog Entry - TEMPERATURE: %s, HUMIDITY: %s" \
            % (temperature, humidity))

        table = "SensorLog"
        items = {
            "TEMPERATURE": temperature,
            "HUMIDITY": humidity
        }

        super().insert(table, items)

    '''
    Count the total entries outside the configured ranges for any given day
    '''
    def count_out_of_range_logs(self, date):
        result = super().execute(self.COUNT_OUT_OF_RANGE_LOGS_SQL, {
            "date": date.strftime(self.DATE_FORMAT),
            "min_temperature": self.__config.get_min_temperature(),
            "max_temperature": self.__config.get_max_temperature(),
            "min_humidity": self.__config.get_min_humidity(),
            "max_humidity": self.__config.get_max_humidity()
        }).fetchone()
        logging.debug("Counted %d entries outside ranges" % result[0])
        return result[0]

    '''
    Select all sensor logs for the supplied date
    '''
    def select_days_logs(self, date):
        results = super().execute(self.SELECT_DAYS_LOGS_SQL, \
            { "date": date.strftime(self.DATE_FORMAT) })

        logs = []
        for result in results:
            logs.append(SensorLog(
                result[self.TEMPERATURE_INDEX], 
                result[self.HUMIDITY_INDEX], 
                result[self.TIMESTAMP_INDEX]))
        return logs