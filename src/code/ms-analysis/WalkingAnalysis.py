import csv
from collections import OrderedDict

import mord
from math import isnan
from matplotlib.dates import *
from scipy.stats import kendalltau

from Analysis import questionAnalysis, IDs, start, end
from Analysis import toNumerical
from Clustering import *
from DatabaseConnector import *
from WalkingTest import gpsToArrays


def walkingAnalysis():
    """
    Analysis of the walking tests done by the participants
    """
    folder = "out/"
    csvDir = folder + "csv/Walking Test Analysis"
    plotDir = folder + "plots/Walking Analysis"
    try:
        os.makedirs(csvDir)
    except OSError:
        pass  # path already exists

    for ID in IDs:
        with open(os.path.join(csvDir, ID + ".csv"), "w") as csvFile:
            writer = csv.writer(csvFile, delimiter=",")
            writer.writerow(("Date", "Distance Walked (m)", "Rating"))
            dictionary = OrderedDict()
            dates = questionAnalysis(ID)

            for (rating, date) in dates:
                dictionary[date] = ("-", rating, None)

            experiments = db_mijnKwik.experiments.find({"userId": ID, "timestamp": {"$gte": start, "$lt": end}}).sort(
                [("timestamp", 1)])
            experiments = list(experiments)
            for exp in experiments:
                value = exp["value"]
                positions = None
                try:
                    # Some weird measurement that are not related to walking are present in the value
                    # Seems like other measurements are also present as experiments
                    positions = value["positions"]
                    positions = list(positions)
                except KeyError:
                    pass

                if positions is not None and len(positions) > 0 and len(positions[0]) is not 0:
                    # verify that the positions do not have zero fields
                    lats, longs, timestamps = gpsToArrays(positions)
                    timestamp = exp["timestamp"]
                    timestamp = timestamp.strftime("%y-%m-%d")
                    success, distance = clustering(lats, longs, timestamps, exp["_id"], timestamp)
                    correspondingDate = [(rating, date) for (rating, date) in dates if timestamp == date]
                    if success:
                        dictionary[timestamp] = (round(distance), correspondingDate[0][0], exp["timestamp"])
                    else:
                        dictionary[timestamp] = ("*", correspondingDate[0][0], exp["timestamp"])

            plt.xlabel("Date")
            plt.ylabel("Distance walked (meters)")
            alpha = 0.5
            lineWidth = 0.15
            s = 100

            X = []  # The measurements
            Y = []  # The ratings
            dataPlotted = False  # indicates if something is plotted

            for date in dictionary:
                (distanceWalked, rating, dateObject) = dictionary[date]

                if isinstance(rating, (unicode, str)) and isinstance(distanceWalked, (int, float)) and rating != "-":
                    X.append(distanceWalked)
                    Y.append(rating)

                    if rating == "Goed":
                        plt.scatter(dateObject, distanceWalked, s=s, color="g", alpha=alpha, linewidth=lineWidth,
                                    edgecolor=almost_black, label="Good day")
                        dataPlotted = True
                    elif rating == "Gemiddeld":
                        plt.scatter(dateObject, distanceWalked, s=s, color="orange", alpha=alpha, linewidth=lineWidth,
                                    edgecolor=almost_black, label="Average day")
                        dataPlotted = True
                    elif rating == "Slecht":
                        plt.scatter(dateObject, distanceWalked, s=s, color="r", alpha=alpha, linewidth=lineWidth,
                                    edgecolor=almost_black, label="Bad day")
                        dataPlotted = True
                    else:
                        print "Something went wrong. The value of rating is ", rating

            plt.gca().xaxis.set_major_formatter(DateFormatter('%y-%m-%d'))
            plt.gca().xaxis.set_major_locator(WeekdayLocator())
            plt.setp(plt.gca().xaxis.get_majorticklabels(), rotation=40)
            fancyPlot()

            if dataPlotted:
                writeToPdf(ID, plotDir)
                (correlation, pvalue) = kendalltau(X[0:len(X) - 1], Y[1:])
                if not isnan(correlation) and not isnan(pvalue):
                    print "Walking Analysis | ID: %s | correlation: %f, pvalue: %f" % (ID, correlation, pvalue)
                    X = np.array(X)
                    X = X.reshape(len(X), 1)
                    Y = map(toNumerical, Y)
                    Y = np.array(Y)
                    model = mord.OrdinalLogistic()
                    try:
                        result = model.fit(X, Y)
                        # print "Coefficient | ", result.coef_  # Coefficient of the first feature (only one feature here)
                        # print result.theta_
                    except IndexError as ex:
                        print ex

                else:
                    print "Incorrect value for correlation or pvalue"

            else:
                plt.close('all')
            for date, (distance, rating, _) in dictionary.items():
                writer.writerow((date, distance, rating))


def main():
    walkingAnalysis()


if __name__ == "__main__":
    main()

__all__ = ['isnan']     # List of imports that otherwise would be classified as not used
