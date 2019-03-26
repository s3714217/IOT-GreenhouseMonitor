import csv
import logging
import os
from config import Config
from datetime import datetime, timedelta
from data.database_initialiser import DatabaseInitialiser
from data.sensor_data_sqlite_repository import SensorDataSqliteRepository
from helpers.readings_validator import ReadingsValidator

class CreateReport:

    DATE_FORMAT = "%Y-%m-%d"

    ONE_DAY_DELTA = timedelta(days = 1)

    REPORTS_DIR = "reports"

    def __init__(self, sensor_data_repository, readings_validator):
        self.__repository = sensor_data_repository
        self.__validator = readings_validator

    '''
    Generate reports for each day that contains readings
    '''
    def generate_reports(self):
        date_span = self.__repository.select_dates_span()
        first_date = datetime.strptime(date_span[0], self.DATE_FORMAT)
        last_date = datetime.strptime(date_span[1], self.DATE_FORMAT)

        # Iterate over each days logs
        date = first_date
        while date <= last_date:
            # simple_date = datetime.strptime(date, self.DATE_FORMAT)
            simple_date = date.strftime(self.DATE_FORMAT)
            self.generate_report(simple_date)
            date += self.ONE_DAY_DELTA

    '''
    Generate report for specified date
    '''
    def generate_report(self, date):
        days_logs = self.__repository.select_days_logs(date)
        if len(days_logs) > 0:
            results = self.__validator.validate_sensor_logs(days_logs)
            # Ensure reports directory exists
            self.create_reports_directory()
            # Ensure report file
            file_path = self.create_report_file()
            # Append status to report
            self.append_status(file_path, date, results)

    '''
    Creates the reports output directory if it does not exist
    '''
    def create_reports_directory(self):
        reports_directory = "%s/%s" % (os.getcwd(), self.REPORTS_DIR)
        if not os.path.exists(reports_directory):
            os.mkdir(reports_directory)

    '''
    Creates the report file
    '''
    def create_report_file(self):
        reports_directory = "%s/%s" % (os.getcwd(), self.REPORTS_DIR)
        file_path = "%s/report.csv" % reports_directory
        if not os.path.exists(file_path):
            # Append titles
            with open(file_path, "a+") as report:
                report.write("Date,Status\r\n")
        return file_path

    '''
    Append the days status to the report
    '''
    def append_status(self, file_path, date, results):
        with open(file_path, "a+") as report:
            if (len(results) == 0):
                report.write("%s,OK\r\n" % date)
            else:
                report.write("%s,BAD: %s\r\n" % (date, ", ".join(results)))

if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG)

    # Initialise database
    DatabaseInitialiser().init_sensor_data()

    # Instantiate dependencies
    config = Config()
    sensor_config = config.get_sensor_config()
    repository = SensorDataSqliteRepository(sensor_config)
    validator = ReadingsValidator(sensor_config)

    # Create report!
    reportMaker = CreateReport(repository, validator)
    reportMaker.generate_reports()