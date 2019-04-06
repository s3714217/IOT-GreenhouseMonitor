import logging
from config import Config
from data.database_initialiser import DatabaseInitialiser
from data.sensor_data_sqlite_repository import SensorDataSqliteRepository
from visualisation.weekly_graph import WeeklyGraph

class Analytics:

    def __init__(self, sensor_data_repository):
        self.__repository = sensor_data_repository

    '''
    Generate a graph of the last weeks minimum and maximum temperatures
    '''
    def generate_weekly_graph(self):
        wg = WeeklyGraph()
        temps = self.__repository.select_week_min_max_temps()
        wg.generate(temps)        

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