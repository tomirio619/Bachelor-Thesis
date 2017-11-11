from geopy.distance import great_circle


def calcDistanceWalked(lats, longs):
    """
    Calculates the distance of the track identified by the latitudes and longitudes
    :param lats: the latitudes
    :param longs: the longitudes
    :return: the distance of the GPS track
    """
    positions = []
    for lat, long in zip(lats, longs):
        coordinate = (lat, long)
        positions.append(coordinate)
    distance = 0
    previousPos = None
    for pos in positions:
        if previousPos is None:
            previousPos = pos
        else:
            previousCoordinate = (previousPos[0], previousPos[1])
            currentCoordinate = (pos[0], pos[1])
            calculatedDistance = great_circle(previousCoordinate, currentCoordinate).meters
            distance += calculatedDistance
            previousPos = pos
    return distance
