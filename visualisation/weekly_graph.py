import calendar
import logging
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta

class WeeklyGraph:

    DATE_FORMAT = "%Y-%m-%d"

    ONE_DAY_DELTA = timedelta(days = 1)

    DATE_INDEX = 0
    MIN_INDEX = 1
    MAX_INDEX = 2

    def __init__(self):
        pass

    '''
    Generate a graph of the last weeks minimum and maximum temperatures
    '''
    def generate(self, temps):
        low = ()
        high = ()
        today = date.today()
        temps_index = 0

        # Plot graph - O(n) algorithm for plotting temps,
        # skipping over days that don't have entries.
        for i in range(0, 7):
            day = today - self.ONE_DAY_DELTA * (6 - i)
            day_str = day.strftime(self.DATE_FORMAT)
            if (temps[temps_index][self.DATE_INDEX] != day_str):
                logging.debug("No entries for date %s" % day_str)
                low += (0,)
                high += (0,)
                continue
            logging.debug("Found entries for date %s" % day_str)
            low += (temps[temps_index][self.MIN_INDEX],)
            high += (temps[temps_index][self.MAX_INDEX],)
            temps_index += 1

        # Init graph
        fig, ax = plt.subplots()
        index = np.arange(len(low))
        fig.tight_layout()

        # Set graph content
        bar_width = 0.4
        low_bars = ax.bar(index, low, bar_width, color="b", label="low")
        high_bars = ax.bar(index + bar_width, high, bar_width, color="r", \
            label="high")

        # Set graph info
        ax.set_title("Min. & Max. Temperatures over the last week")
        ax.set_xlabel("Day of the Week")
        ax.set_ylabel("Temperature")
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels((
            calendar.day_abbr[(today - self.ONE_DAY_DELTA * 6).weekday()],
            calendar.day_abbr[(today - self.ONE_DAY_DELTA * 5).weekday()],
            calendar.day_abbr[(today - self.ONE_DAY_DELTA * 4).weekday()],
            calendar.day_abbr[(today - self.ONE_DAY_DELTA * 3).weekday()],
            calendar.day_abbr[(today - self.ONE_DAY_DELTA * 2).weekday()],
            calendar.day_abbr[(today - self.ONE_DAY_DELTA).weekday()],
            calendar.day_abbr[today.weekday()]
        ))
        ax.legend()

        # Save graph to file
        plt.savefig("weeks-temps_bar-graph.png", bbox_inches="tight");