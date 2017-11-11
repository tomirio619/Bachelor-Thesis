from __future__ import division

import numpy as np
from scipy import interpolate
from scipy.signal import savgol_filter


def smooth(lats, longs, timestamps):
    """
    Given the above paramaters, creates a smoothed line through the GPS coordinates
    :param lats:        The latitudes
    :param longs:       The longitudes
    :param timestamps:  The timestamps
    :return:            x and y arrays resulting from lineair interpolation, and x and y arrays resulting from application
    of the savgol filter on this lineair interpolation
    """
    y = lats        # the latitudes
    x = longs       # the longitudes
    t = timestamps  # the timestamps
    t = np.array(t)
    nt = np.linspace(0, 1, 1000)
    t = t - t[0]
    t /= t[-1]
    fx2 = interpolate.interp1d(t, x, kind="linear")
    fy2 = interpolate.interp1d(t, y, kind="linear")
    x2 = fx2(nt)
    y2 = fy2(nt)
    newx2 = savgol_filter(x2, 157, 1)
    newy2 = savgol_filter(y2, 157, 1)
    return x2, y2, newx2, newy2
