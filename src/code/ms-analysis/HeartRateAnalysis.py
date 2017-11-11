import csv
import math
from collections import OrderedDict
from itertools import groupby

import mord
import numpy as np
from matplotlib.dates import *
from scipy.stats import kendalltau

from Analysis import *
from BetterPlots import fancyPlot, fancyBoxPlot
from IO import *

# Global stuff
almost_black = "#262626"


def heartRateAnalysis():
    """
    Analysis of the heart rates of our participants per day
    """
    # heart rate has mtype 1
    folder = "out/"
    csvDir = folder + "csv/Heart Rate"
    plotDir = folder + "plots/Heart Rate plots"
    boxPlotDir = folder + "plots/Heart Rate boxplots"

    measurementDictionary = OrderedDict()
    try:
        os.makedirs(csvDir)
    except OSError:
        pass  # path already exists

    for (ID, pid, device) in basisPeak + fitBit:
        measurements = None
        if device == "basispeak":
            measurements = db.measurements.find({"pid": pid, "mtype": 1, "date": {"$gte": start, "$lt": end}}).sort(
                [("date", 1)])
            measurements = list(measurements)
        elif device == "fitbit":
            measurements = db.diaFitBitPatients.find(
                {"pid": pid, "mtype": 1, "date": {"$gte": start, "$lt": end}}).sort(
                [("date", 1)])
            measurements = list(measurements)
        elif device == "microsoftband":
            measurements = []
            # The measurements for this device were not present in the database while writing this code

        keys = []
        for key, group in groupby(measurements, lambda x: x["date"].strftime("%y-%m-%d")):
            # group the measurements based on date
            keys.append(key)
            measurementDictionary[key] = [el for el in group
                                          if isinstance(el["value"], int) and
                                          not math.isnan(el["value"]) and
                                          el["value"] == el["value"]]
        # Create a list witch contains list with all the measurement of the same date
        measurementsPerDate = []
        dateObjects = []

        for key in keys:
            dateMeasurement = [measurement["value"] for measurement in measurementDictionary[key]]
            measurementsPerDate.append(dateMeasurement)

            # Finding the date objects
            if dateMeasurement:
                newDate = measurementDictionary[key][0]['date']
                if not dateObjects:
                    dateObjects.append(newDate)
                else:
                    similarDates = [date for date in dateObjects if
                                    date.year == newDate.year and
                                    date.month == newDate.month and
                                    date.day == newDate.day
                                    ]
                    if not similarDates:
                        dateObjects.append(newDate)
        # The boxplot
        fig = plt.figure()
        plt.xlabel("Date")
        plt.ylabel("Heart rate")
        plt.title("ID: %s" % ID)
        bp = plt.gca().boxplot(measurementsPerDate, patch_artist=True)
        fig.autofmt_xdate()
        plt.xticks(np.arange(1, len(keys) + 1), keys, rotation=45)
        fancyBoxPlot(bp)
        writeToPdf(ID, boxPlotDir)

        ratings = questionAnalysis(ID)

        with open(os.path.join(csvDir, ID + ".csv"), "w") as csvFile:
            writer = csv.writer(csvFile, delimiter=",")
            writer.writerow(("Date", "Rating", "Median", "Average", "Standard Deviation"))

            X = []  # contains the measurements
            Y = []  # contains the ratings
            intersectedDates = np.intersect1d([el[1] for el in ratings], keys)

            for (rating, date) in ratings:
                if date in intersectedDates:
                    measurements = [measurement["value"] for measurement in measurementDictionary[date]]
                    measurements = sorted(measurements)
                    writer.writerow((
                        date,
                        rating,
                        np.median(measurements),
                        round(np.average(measurements)),
                        round(np.std(measurements), 2)
                    ))
                    measurements = measurements[0: int(len(measurements) * 0.05)]
                    stableHeartRate = np.average(measurements)

                    Y.append(rating)
                    X.append(stableHeartRate)

                    alpha = 0.5
                    lineWidth = 0.15
                    s = 100
                    dateObject = measurementDictionary[date][0]['date']
                    # Normal plotting
                    if rating == "Goed":
                        plt.scatter(dateObject, stableHeartRate, s=s, color="g", alpha=alpha, linewidth=lineWidth,
                                    edgecolor=almost_black, label="Good day")
                    elif rating == "Gemiddeld":
                        plt.scatter(dateObject, stableHeartRate, s=s, color="orange", alpha=alpha,
                                    linewidth=lineWidth,
                                    edgecolor=almost_black, label="Average day")
                    elif rating == "Slecht":
                        plt.scatter(dateObject, stableHeartRate, s=s, color="r", alpha=alpha, linewidth=lineWidth,
                                    edgecolor=almost_black, label="Bad day")

            plt.gca().xaxis.set_major_formatter(DateFormatter('%y-%m-%d'))
            plt.gca().xaxis.set_major_locator(WeekdayLocator())
            plt.setp(plt.gca().xaxis.get_majorticklabels(), rotation=40)
            plt.xlabel("Date")
            plt.ylabel("Heart rate")
            fancyPlot(dateLimit=True)
            writeToPdf(ID, plotDir)
            (correlation, pvalue) = kendalltau(X[0:len(X) - 1], Y[1:])
            if -1 <= correlation <= 1:
                print "Walking Analysis | ID: %s | pid : %s | correlation: %f, pvalue: %f" % (
                    ID, pid, correlation, pvalue)

            # Use Ordinal Regression, see Mord
            # https://en.wikipedia.org/wiki/Ordinal_regression
            X = np.array(X)
            X = X.reshape(len(X), 1)
            Y = map(toNumerical, Y)
            Y = np.array(Y)
            model = mord.OrdinalLogistic()
            """
            fit() calls threshold_fit(), which makes use of the optimize.minimize() method.
            To prevent the "Desired error not necessarily achieved due to precision loss" message,
            add add the following paramter to this function: optimize.minize(..., ..., method='Nelder-Mead')
            """
            result = model.fit(X, Y)
            # TODO If the ratings only contain two distinct values, an error occurs
            # print "Coefficient | ", result.coef_  # Coefficient of the first feature (only one feature here)
            # print result.theta_


def main():
    heartRateAnalysis()


if __name__ == "__main__":
    main()
