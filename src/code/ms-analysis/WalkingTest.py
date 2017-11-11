from __future__ import division

import numpy as np
from sklearn.covariance import EllipticEnvelope

from BetterPlots import fancyPlot
from Clustering import clustering
from DatabaseConnector import *
from DistanceCalculator import calcDistanceWalked
from IO import *
from Smoothing import smooth

# Global stuff
almost_black = "#262626"


def outlierDetection(IDs):
    """
    For given IDs, calculated the distance walked.
    This is done by using outlier detection.
    The results are also plotted, and coordinates are written to output files for plotting
    :param IDs the IDs of the users
    """
    for ID in IDs:
        experiments = db_mijnKwik.experiments.find({"userId": ID}).sort([("timestamp", -1)])
        experiments = list(experiments)
        for exp in experiments:
            positions = exp["value"]["positions"]
            timestamp = exp["timestamp"]
            print(timestamp.strftime("%y-%m-%d %H:%M:%S"))
            PlotEllipticOutliers(positions, exp["_id"], timestamp.strftime("%y-%m-%d %H:%M:%S"))


def PlotEllipticOutliers(rawPositions, ID, timestmp):
    """
    This method is used for outlier detection on a straight track.
    Uses the EllipticEnvelope object from Scikit-learn
    :param rawPositions:    The raw GPS positions
    :param ID:              The ID of the user
    :param timestmp:        The timestamp
    """
    folder = "out/"
    plotDir = folder + "plots/Walking Test"

    lats = []
    longs = []
    timestamps = []
    for pos in rawPositions:
        lat = pos["latitude"]
        long = pos["longitude"]
        timestamp = pos["timestamp"]
        lats.append(lat)
        longs.append(long)
        timestamps.append(timestamp)

    classifiers = {
        "Robust Covariance Estimator": EllipticEnvelope(contamination=0.08, support_fraction=0.8)
    }
    alpha = 0.5
    linewidth = 0.15

    classifierName = "Robust Covariance Estimator"
    classifier = classifiers[classifierName]
    X = zip(lats, longs)
    xx1, yy1 = np.meshgrid(np.linspace(min(lats), max(lats), 1000), np.linspace(min(longs), max(longs), 1000))
    classifier.fit(X)
    Z1 = classifier.decision_function(np.c_[xx1.ravel(), yy1.ravel()])
    Z1 = Z1.reshape(xx1.shape)
    CS = plt.contour(xx1, yy1, Z1, levels=[0], linewidths=1, colors="g")
    CS.collections[0].set_label(classifierName)
    plt.scatter(lats, longs, s=50, alpha=alpha, linewidth=linewidth, edgecolor=almost_black, color="steelblue",
                label="GPS coordinate")
    plt.autoscale(enable=True, axis="both")
    filteredPositions = []

    for lat, long, timestamp in zip(lats, longs, timestamps):
        z = classifier.decision_function(np.c_[lat, long])
        # Check if coordinate (lat, long) is within the ellipse
        if z > 0:
            filteredPositions.append((lat, long, timestamp))

    y = zip(*filteredPositions)[0]  # the latitudes
    x = zip(*filteredPositions)[1]  # the longitudes
    t = zip(*filteredPositions)[2]  # the timestamps

    x2, y2, newx2, newy2 = smooth(y, x, t)
    plt.plot(y2, x2, label="Linear Interpolation")
    totalDistance = calcDistanceWalked(newy2, newx2)

    plt.plot(newy2, newx2, label="Savgol Filter", color="r")
    plt.title("Timestamp: %s\n Calculated distance: %i meters" % (timestmp, totalDistance))
    plt.xlabel("Latitude")
    plt.ylabel("Longitude")
    fancyPlot()
    writeToPdf(ID, plotDir)


def gpsToArrays(rawPositions):
    """
    Gets the latitudes and longitudes from raw positions
    :param rawPositions: the raw positions
    :return: the latitudes, longitudes and timestamps
    """
    lats = []
    longs = []
    timestamps = []
    for pos in rawPositions:
        lat = pos["latitude"]
        long = pos["longitude"]
        timestamp = pos["timestamp"]
        lats.append(lat)
        longs.append(long)
        timestamps.append(timestamp)
    return lats, longs, timestamps


def experimentAnalysis():
    """
    Start the analysis of the walking tests did by me
    """
    TomuserId = "cDb6t5p66vyGDpA2x"
    AnnieuserId = "Aq2iqK4YKyQBFEeDC"
    IDs = [TomuserId
           # ,AnnieuserId
           ]
    for ID in IDs:
        experiments = db_mijnKwik.experiments.find({"userId": ID}).sort([("timestamp", -1)])
        experiments = list(experiments)[0:5]
        for exp in experiments:
            positions = exp["value"]["positions"]
            lats, longs, timestamps = gpsToArrays(positions)
            timestamp = exp["timestamp"]
            timestamp = timestamp.strftime("%y-%m-%d %H:%M:%S")
            clustering(lats, longs, timestamps, exp["_id"], timestamp, multiPDF=False)


def main():
    experimentAnalysis()
    outlierDetection(["cDb6t5p66vyGDpA2x", "Aq2iqK4YKyQBFEeDC"])


if __name__ == "__main__":
    main()
