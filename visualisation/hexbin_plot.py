import matplotlib.pyplot as plt
import seaborn as sns

class HexbinPlot:

    def __init__(self):
        pass

    '''
    Generates a Hexbin Plot for the current days data, this should show any
    correlation between temperature and humidity
    '''
    def generate(self, data):
        x = ()
        y = ()

        sns.set(style="ticks")

        for log in data:
            x += (log.get_humidity(),)
            y += (log.get_temperature(),)

        ax = sns.jointplot(x, y, kind="hex", color="#4CB391")
        plt.savefig("days-readings_hexbin-plot.png", bbox_inches="tight");