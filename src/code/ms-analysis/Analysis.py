from __future__ import division

import datetime
from operator import itemgetter

import matplotlib

from DatabaseConnector import *

start = datetime.datetime(2016, 3, 25, 0, 0, 0, 0)
end = datetime.datetime(2016, 5, 17, 0, 0, 0, 0)

matplotlib.rc('font', **{'sans-serif': 'Arial',
                         'family': 'sans-serif'})

IDs = ["gGSWzh5PnqgFdCpq4",
       "S2usWtx8WXPe8S88r",
       "oGTtb7DQu4ewMBinx",
       "dW4YzJQEaidmyhsuY",
       "2Dy2uFf3aw6jv9r5u"
       ]

basisPeak = [("dW4YzJQEaidmyhsuY", "1015", "basispeak"), ("2Dy2uFf3aw6jv9r5u", "1014", "basispeak")]
fitBit = [("gGSWzh5PnqgFdCpq4", "hidden_email", "fitbit"),
          ("S2usWtx8WXPe8S88r", "hidden_email", "fitbit")]
microsoftBand = []


def toTimeStamp(dt, epoch=datetime.datetime(1970, 1, 1)):
    """
    Transforms a given datetime object to a timestamp.
    :param dt: the datetime object
    :param epoch: the date from which will be used as zero point
    :return: the difference in milliseconds between dt and epoch (dt - epoch)
    """
    td = dt - epoch
    return (td.microseconds + (td.seconds + td.days * 86400) * 10 ** 6) / 10 ** 6


def toNumerical(rating):
    """
    Convert a given rating to a numerical value
    :param rating: The rating
    :return: Numerical value
    """
    if rating == "Goed":
        return 2
    elif rating == "Gemiddeld":
        return 1
    elif rating == "Slecht":
        return 0


def questionAnalysis(ID):
    """
    For a given ID, returns all the ratings for the specified period
    :return: list with (rating, date) tuples
    """
    msTodayId = "FDSxWja8uuMNGoeJE"
    observations = db_mijnKwik.observations.find(
        {"userId": ID, "questionId": msTodayId, "timestamp": {"$gte": start, "$lt": end}}).sort(
        [("timestamp", -1)])
    observations = list(observations)
    dateRatings = []

    for observation in observations:
        value = observation["value"]
        date = observation["timestamp"]
        date = date.strftime("%y-%m-%d")
        dateRatings.append((value, date))

    # remove duplicate dates and sort on increasing date
    duplicateDatesRemoved = []
    for (rating, date) in set(dateRatings):
        if not duplicateDatesRemoved:
            duplicateDatesRemoved.append((rating, date))
        elif date not in zip(*duplicateDatesRemoved)[1]:
            duplicateDatesRemoved.append((rating, date))

    return sorted(duplicateDatesRemoved, key=itemgetter(1))
