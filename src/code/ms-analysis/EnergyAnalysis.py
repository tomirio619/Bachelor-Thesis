from collections import OrderedDict
from itertools import groupby

import numpy as np
from matplotlib.dates import *
from scipy.stats import kendalltau
from sklearn.linear_model import LogisticRegression

from Analysis import *
from BetterPlots import fancyPlot
from IO import *
import math

# Global stuff
almost_black = "#262626"


def energyAnalysis():
    """
    Analysis of the energy analysis of our participants per day
    """
    energyQuestionId = "HanWRjvZe8PiLvfD4"
    folder = "out/"
    plotDir = folder + "plots/Energy Analysis plots"
    try:
        os.makedirs(plotDir)
    except OSError:
        pass  # path already exists

    for ID in IDs:
        experiments = db_mijnKwik.observations.find({"userId": ID, "questionId": energyQuestionId,
                                                     "timestamp": {"$gte": start, "$lt": end}}).sort([("timestamp", 1)])
        experiments = list(experiments)

        X = []  # The measurements
        Y = []  # The ratings
        keys = []

        measurementDictionary = OrderedDict()
        ratings = questionAnalysis(ID)

        for key, group in groupby(experiments, lambda x: x["timestamp"].strftime("%y-%m-%d")):
            # group the measurements based on date
            keys.append(key)
            measurementDictionary[key] = [el for el in group]

        plt.xlabel("Date")
        plt.ylabel("Energy Level")
        alpha = 0.5
        lineWidth = 0.15
        s = 100

        intersectedDate = np.intersect1d([el[1] for el in ratings], keys)
        for (rating, date) in ratings:
            if date in intersectedDate:

                measurements = measurementDictionary[date]
                dateObject = measurements[0]['timestamp']
                energyRating = np.average([measurement['value'] for measurement in measurements])
                X.append(energyRating)
                Y.append(rating)

                if rating == "Goed":
                    plt.scatter(dateObject, energyRating, s=s, color="g", alpha=alpha, linewidth=lineWidth,
                                edgecolor=almost_black, label="Good day")
                elif rating == "Gemiddeld":
                    plt.scatter(dateObject, energyRating, s=s, color="orange", alpha=alpha, linewidth=lineWidth,
                                edgecolor=almost_black, label="Average day")
                elif rating == "Slecht":
                    plt.scatter(dateObject, energyRating, s=s, color="r", alpha=alpha, linewidth=lineWidth,
                                edgecolor=almost_black, label="Bad day")
                else:
                    print "Something went wrong. The value of rating is ", rating

        plt.gca().xaxis.set_major_formatter(DateFormatter('%y-%m-%d'))
        plt.gca().xaxis.set_major_locator(WeekdayLocator())
        plt.setp(plt.gca().xaxis.get_majorticklabels(), rotation=40)
        fancyPlot(dateLimit=True)
        writeToPdf(ID, plotDir)
        """
        To predict the next day, we need to drop certain elements in the list.
        Lets look at an example.
        X: 4,2,4,5      (The measurements)
        Y: G,A,B,A      (The ratings)

        By dropping the last element of the "X" array
        and dropping the first element of the "Y" array we get the following lists:
        X: 4,2,4
        Y: A,B,A

        This is exactly what we need!
        PS: we need to make sure that all the dates are consecutive
        """
        (correlation, pvalue) = kendalltau(X[0:len(X) - 1], Y[1:])
        if not math.isnan(correlation) and not math.isnan(pvalue):
            print "Walking Analysis | ID: %s | correlation: %f, pvalue: %f" % (ID, correlation, pvalue)

        X = np.array(X).T
        # Because energy rating is nominal data, we can use normal logistic regression
        logic = LogisticRegression()
        logic.fit(X.reshape(len(X), 1), Y)
        print logic.coef_  # Coefficient of the first feature (only one feature here)


def main():
    energyAnalysis()


if __name__ == "__main__":
    main()
