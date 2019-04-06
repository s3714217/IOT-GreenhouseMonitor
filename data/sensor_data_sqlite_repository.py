import logging
import os
from datetime import datetime
from data.sqlite_repository import SqliteRepository
from models.sensor_log import SensorLog

'''
SQLite repository to handle persisting sensor data
'''
class SensorDataSqliteRepository(SqliteRepository):

    DATE_FORMAT = "%Y-%m-%d"

    TEMPERATURE_INDEX = 0
    HUMIDITY_INDEX = 1
    TIMESTAMP_INDEX = 2

    MIN_DATE_INDEX = 0
    MAX_DATE_INDEX = 1

    SELECT_DAYS_LOGS_SQL = "SELECT temperature, humidity, timestamp \
        FROM SensorLog \
        WHERE timestamp >= DATE(:date) \
        AND timestamp < DATE(:date, '+1 day')"

    SELECT_DATE_SPAN_SQL = "SELECT DATE(MIN(timestamp), 'start of day'), \
        DATE(MAX(timestamp), 'start of day') FROM SensorLog"

    COUNT_OUT_OF_RANGE_LOGS_SQL = "SELECT COUNT(*) FROM SensorLog \
        WHERE timestamp BETWEEN DATE(:date) AND DATE(:date, '+1 day') \
        AND (temperature NOT BETWEEN :min_temperature AND :max_temperature \
        OR humidity NOT BETWEEN :min_humidity AND :max_humidity)"

    COUNT_NOTIFICATIONS_SENT_SQL = "SELECT COUNT(*) FROM NotificationLog \
        WHERE timestamp BETWEEN DATE(:date) AND DATE(:date, '+1 day')"

    SELECT_WEEK_MIN_MAX_TEMPS_SQL = "SELECT Date(timestamp) AS 'Date', \
        MIN(Temperature) AS 'Min', MAX(Temperature) AS 'Max' FROM SensorLog \
        WHERE Timestamp >= DATE('now', 'localtime', '-6 day') \
        AND Timestamp < DATE('now', 'localtime', '+1 day') \
        GROUP BY Date(Timestamp) ORDER BY Timestamp ASC"

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
    Insert an entry into the NotificationLog table
    '''
    def insert_notification_log(self):
        logging.debug("Inserting SensorLog Entry")

        table = "NotificationLog"
        super().insert(table, None)

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
    Count the total entries in the NotificationLog table for any given day
    '''
    def count_notifications_sent(self, date):
        result = super().execute(self.COUNT_NOTIFICATIONS_SENT_SQL, {
            "date": date.strftime(self.DATE_FORMAT)}).fetchone()
        logging.debug("Counted %d notification(s) sent" % result[0])
        return result[0]

    '''
    Select all sensor logs for the supplied date
    '''
    def select_days_logs(self, date):
        results = super().execute(self.SELECT_DAYS_LOGS_SQL, { "date": date })

        logs = []
        for result in results:
            logs.append(SensorLog(
                result[self.TEMPERATURE_INDEX], 
                result[self.HUMIDITY_INDEX], 
                result[self.TIMESTAMP_INDEX]))
        return logs

    '''
    Select the SensorLog's entries min and max date
    '''
    def select_dates_span(self):
        results = super().execute(self.SELECT_DATE_SPAN_SQL).fetchone()
        logging.debug("Selected dates span - MIN: %s, MAX: %s" % \
            (results[self.MIN_DATE_INDEX], results[self.MAX_DATE_INDEX]))
        return results

    '''
    Select the min and max temps for the past week, including today
    '''
    def select_week_min_max_temps(self):
        results = super().execute(self.SELECT_WEEK_MIN_MAX_TEMPS_SQL)
        logging.debug("Selected weeks min max temps")
        temps = []
        for result in results:
            temps.append(result)
        return temps