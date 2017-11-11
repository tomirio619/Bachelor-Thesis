import csv
from collections import OrderedDict
from itertools import groupby

import mord
import numpy as np
from matplotlib.dates import *
from scipy.stats import kendalltau

from Analysis import *
from BetterPlots import fancyPlot
from IO import *

# Global stuff
almost_black = "#262626"


def sleepAnalysis():
    """
    Analysis of the sleep duration of our participants per day
    """
    csvDir = "out/csv/Sleep Analysis"
    plotDir = "out/plots/Sleep Analysis"
    measurementDictionary = OrderedDict()
    try:
        os.makedirs(csvDir)
    except OSError:
        # path already exists
        pass

    for (ID, pid, device) in basisPeak + fitBit:
        measurements = None
        if device == "basispeak":
            measurements = db.measurements.find({"pid": pid, "mtype": 7, "date": {"$gte": start, "$lt": end}}).sort(
                [("date", 1)])
            measurements = list(measurements)

        elif device == "fitbit":
            measurements = db.diaFitBit.find({"pid": pid, "mtype": 7, "date": {"$gte": start, "$lt": end}}).sort(
                [("date", 1)])
            measurements = list(measurements)

        elif device == "microsoftband":
            measurements = []

        keys = []
        if device == "basispeak":
            for key, group in groupby(measurements, lambda x: x["end"].strftime("%y-%m-%d")):
                # group the measurements based on date
                keys.append(key)
                measurementDictionary[key] = [el for el in group]
        elif device == "fitbit":
            for measurement in measurements:
                measurement['end'] = measurement['date']
                measurement['value'] /= 60.0
                date = measurement['date'].strftime("%y-%m-%d")
                keys.append(date)
                measurementDictionary[date] = [measurement]

        ratings = questionAnalysis(ID)
        with open(os.path.join(csvDir, ID + ".csv"), "w") as csvFile:
            writer = csv.writer(csvFile, delimiter=",")
            writer.writerow(("Date", "Rating", "Duration"))
            intersectedDates = np.intersect1d([el[1] for el in ratings], keys)
            sleepDurationPerDate = OrderedDict()

            for date in np.union1d([el[1] for el in ratings], keys):
                filteredRatings = [el for el in ratings if el[1] == date]
                if date in keys:
                    for measurement in measurementDictionary[date]:
                        duration = round(measurement['value'], 2)
                        if filteredRatings and duration != 0:
                            # We found a rating for this date
                            rating = filteredRatings[0][0]

                            try:
                                (rating, sleepDuration, dateObject) = sleepDurationPerDate[date]
                                sleepDurationPerDate[date] = (rating, sleepDuration + duration, dateObject)
                            except KeyError:
                                sleepDurationPerDate[date] = (rating, duration, measurement['date'])

                            writer.writerow((
                                measurement['end'].strftime("%y-%m-%d %H:%M:%S"),
                                rating,
                                duration
                            ))
                        else:
                            # No rating found, write "-" as rating
                            writer.writerow((
                                measurement['end'].strftime("%y-%m-%d %H:%M:%S"),
                                "-",
                                duration
                            ))
                else:
                    # This date had no measurement
                    if filteredRatings:
                        rating = ratings[0][0]
                        writer.writerow((
                            date,
                            rating,
                            "-"
                        ))
                    else:
                        writer.writerow((
                            date,
                            "-",
                            "-"
                        ))

            alpha = 0.5
            lineWidth = 0.15
            s = 100
            X = []  # contains the measurements
            Y = []  # contains the ratings

            for date in sleepDurationPerDate:
                (rating, totalSleepDuration, dateObject) = sleepDurationPerDate[date]
                X.append(totalSleepDuration)
                Y.append(rating)
                if rating == "Goed":
                    plt.scatter(dateObject, totalSleepDuration, s=s, color="g", alpha=alpha, linewidth=lineWidth,
                                edgecolor=almost_black, label="Good day")
                elif rating == "Gemiddeld":
                    plt.scatter(dateObject, totalSleepDuration, s=s, color="orange", alpha=alpha, linewidth=lineWidth,
                                edgecolor=almost_black, label="Average day")
                elif rating == "Slecht":
                    plt.scatter(dateObject, totalSleepDuration, s=s, color="r", alpha=alpha, linewidth=lineWidth,
                                edgecolor=almost_black, label="Bad day")

            plt.gca().xaxis.set_major_formatter(DateFormatter('%y-%m-%d'))
            plt.gca().xaxis.set_major_locator(WeekdayLocator())
            plt.setp(plt.gca().xaxis.get_majorticklabels(), rotation=40)
            plt.xlabel("Date")
            plt.ylabel("Sleep duration (hours)")
            fancyPlot(dateLimit=True)
            writeToPdf(ID, plotDir)

            (correlation, pvalue) = kendalltau(X[0:len(X) - 1], Y[1:])
            if -1 <= correlation <= 1:
                print "Walking Analysis | ID: %s | pid : %s | correlation: %f, pvalue: %f" % (
                    ID, pid, correlation, pvalue)

            X = np.array(X)
            X = X.reshape(len(X), 1)
            Y = map(toNumerical, Y)
            Y = np.array(Y)
            model = mord.OrdinalLogistic()
            try:
                result = model.fit(X, Y)
                # Coefficient of the first feature (only one feature here)
                print "Coefficient | ", result.coef_
                # print result.theta_
            except Exception as ex:
                print ex
                pass


def main():
    sleepAnalysis()


if __name__ == "__main__":
    main()
