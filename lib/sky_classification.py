import matplotlib.pyplot as plt
from bokeh.plotting import figure
import numpy as np


def sky_classification(kb):

    """
        Print kb plot

    """
    hist, edges = np.histogram(kb, density=True, bins=50)


    p = figure(title='Direct fraction kb', x_axis_label='kb',
               y_axis_label='density')

    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)

    return p
