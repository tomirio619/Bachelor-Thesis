import os

import matplotlib.pyplot as plt


def writeToFile(filename, dir, lats, longs):
    """
    Writes latitudes and longitudes to the subfolder "output/filename"
    :param dir:         The name of the directory
    :param filename:    The filename
    :param lats:        The latitudes
    :param longs:       The longitudes
    """
    try:
        os.makedirs(dir)
    except OSError:
        # path already exists
        pass
    with open(os.path.join(dir, filename) + ".txt", "w") as output:
        for lat, long in zip(lats, longs):
            output.write("%s, %s \n" % (lat, long))


def writeToPdf(filename, dir, multiPDF=False):
    """
    Write figure to PDF
    :param multiPDF:    indicates if a multiPDF is used
    :param filename:    the filename
    :param dir:         the name of the dir
    """
    try:
        os.makedirs(dir)
    except OSError:
        # path already exists
        pass
    plt.savefig(os.path.join(dir, filename + ".pdf"))
    if not multiPDF:
        plt.cla()
        plt.clf()
        plt.close('all')
