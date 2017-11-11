from collections import OrderedDict

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

from Analysis import start, end

rcParams.update({'figure.autolayout': True})

# Global stuff
almost_black = "#262626"


def fancyPlot(scatterpoints=1, numpoints=1, dateLimit=False):
    """
    VISUAL TWEAKS
    """
    ax = plt.gca()  # The current axis
    # Remove top and right axes lines ("spines")
    spines_to_remove = ['top', 'right']
    for spine in spines_to_remove:
        plt.gca().spines[spine].set_visible(False)

    # Remove top axes and right axes ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    # For remaining spines, thin out their line and change the black to a slightly off-black dark grey
    spines_to_keep = ['bottom', 'left']
    for spine in spines_to_keep:
        ax.spines[spine].set_linewidth(0.5)
        ax.spines[spine].set_color(almost_black)

    # Change the labels to the off-black
    ax.xaxis.label.set_color(almost_black)
    ax.yaxis.label.set_color(almost_black)

    # Change the axis title to off-black
    ax.title.set_color(almost_black)

    if dateLimit:
        ax.set_xlim([start, end])

    # Remove the line around the legend box, and instead fill it with a light grey
    # Also only use one point for the scatterplot legend
    # Also remove redundant labels,
    # see http://stackoverflow.com/questions/13588920/stop-matplotlib-repeating-labels-in-legend
    handles, labels = ax.get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    legend = ax.legend(by_label.values(), by_label.keys(), frameon=True, scatterpoints=scatterpoints,
                       numpoints=numpoints, loc="best", framealpha=0.5)
    light_grey = np.array([float(248) / float(255)] * 3)
    rect = legend.get_frame()
    rect.set_facecolor(light_grey)
    rect.set_linewidth(0.0)

    # Change the legend label colors to almost black, too
    texts = legend.texts
    for t in texts:
        t.set_color(almost_black)

    plt.tight_layout()


def fancyBoxPlot(bp):
    """
    Customize the boxplot
    :param bp: the boxplot variable
    """
    ax = plt.gca()  # Get current axis
    # Remove top axes and right axes ticks
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    # change outline color, fill color and linewidth of the boxes
    for box in bp['boxes']:
        # change outline color
        box.set(color='steelblue', linewidth=1)
        # change fill color
        box.set(facecolor='darkgrey')

    # change color and linewidth of the whiskers
    for whisker in bp['whiskers']:
        whisker.set(color='steelblue', linewidth=1)

    # change color and linewidth of the caps
    for cap in bp['caps']:
        cap.set(color='steelblue', linewidth=1)

    # change color and linewidth of the medians
    for median in bp['medians']:
        median.set(color='black', linewidth=1.2)

    # change the style of fliers (outliers) and their fill
    for flier in bp['fliers']:
        flier.set(marker='o', markerfacecolor='Tomato', alpha=0.5, markersize=4, linewidth=0.15,
                  markeredgecolor=almost_black)

    plt.tight_layout()
