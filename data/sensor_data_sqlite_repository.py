import logging
import os
from datetime import datetime
from data.sqlite_repository import SqliteRepository
from helpers.dates_index import DatesIndex
from helpers.sensor_log_index import SensorLogIndex
from models.sensor_log import SensorLog

'''
SQLite repository to handle persisting sensor data
'''
class SensorDataSqliteRepository(SqliteRepository):

    DATE_FORMAT = "%Y-%m-%d"

    # These would normally be stored procs!
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
        WHERE timestamp BETWEEN DATE(:date) AND DATE(:date, '+1 day') \
        AND Device IS NULL"

    COUNT_DEVICE_NOTIFICATIONS_SENT_SQL = "SELECT COUNT(*) FROM NotificationLog \
        WHERE timestamp BETWEEN DATE(:date) AND DATE(:date, '+1 day') \
        AND Device = :device"

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
    def insert_sensor_log(self, sensor_log):

        logging.debug("Inserting SensorLog Entry - TEMPERATURE: %s, HUMIDITY: %s" \
            % (sensor_log.get_temperature(), sensor_log.get_humidity()))

        table = "SensorLog"
        items = {
            "Temperature": sensor_log.get_temperature(),
            "Humidity": sensor_log.get_humidity()
        }

        super().insert(table, items)

    '''
    Insert an entry into the NotificationLog table
    '''
    def insert_notification_log(self, device = None):
        logging.debug("Inserting SensorLog Entry")

        table = "NotificationLog"
        if device is None:
            super().insert(table, None)
        else:
            device = "'%s'" % device
            super().insert(table, { "Device": device })

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
    Count the total entries in the NotificationLog table for any given day,
    optionally supplying a device
    '''
    def count_notifications_sent(self, date, device = None):
        # Determine sql to run
        sql = self.COUNT_NOTIFICATIONS_SENT_SQL \
            if device is None else self.COUNT_DEVICE_NOTIFICATIONS_SENT_SQL

        # Execute sql
        result = super().execute(sql, {
            "date": date.strftime(self.DATE_FORMAT),
            "device": device}).fetchone()
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
                result[SensorLogIndex.TEMPERATURE], 
                result[SensorLogIndex.HUMIDITY], 
                result[SensorLogIndex.TIMESTAMP]))
        return logs

    '''
    Select the SensorLog's entries min and max date
    '''
    def select_dates_span(self):
        results = super().execute(self.SELECT_DATE_SPAN_SQL).fetchone()
        logging.debug("Selected dates span - MIN: %s, MAX: %s" \
            % (results[DatesIndex.MIN], results[DatesIndex.MAX]))
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