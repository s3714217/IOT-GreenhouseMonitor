#!/usr/bin/env python3
import logging
from config import Config
from data.database_initialiser import DatabaseInitialiser
from data.sensor_data_sqlite_repository import SensorDataSqliteRepository
from datetime import date
from visualisation.hexbin_plot import HexbinPlot
from visualisation.weekly_graph import WeeklyGraph

class Analytics:

    def __init__(self, sensor_data_repository):
        self.__repository = sensor_data_repository

    '''
    Generate a graph of the last weeks minimum and maximum temperatures
    '''
    def generate_weekly_graph(self):
        graph = WeeklyGraph()
        data = self.__repository.select_week_min_max_temps()
        graph.generate(data)

    '''
    Generate a hexbin plot of the days temperature and humidity
    '''
    def generate_hexbin_plot(self):
        plot = HexbinPlot()
        data = self.__repository.select_days_logs(date.today())
        plot.generate(data)

if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG)

    # Initialise database
    DatabaseInitialiser().init_sensor_data()

    # Instantiate dependencies
    config = Config()
    sensor_config = config.get_sensor_config()
    repository = SensorDataSqliteRepository(sensor_config)

    # Generate graphs
    analytics = Analytics(repository)
    analytics.generate_weekly_graph()
    analytics.generate_hexbin_plot()