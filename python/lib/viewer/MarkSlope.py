import matplotlib.pyplot as plt, numpy as np
from mpltools import annotation
def mark_slope(ax, x1, y1, slope=(2, 1),
        text_kwargs={'color': 'black'},
        poly_kwargs={'facecolor': (0., 0., 0)},
        **kwargs):
    '''all parameters are passed to mpltools.annotation.slope_marker
    slope can equivalently be, for example, 2 or (2,1).

    Example Usage:
mark_slope(ax, x1, y1)
#...or better yet
annotation.slope_marker(origin=(x1, y1),
                        slope=3,#(3, 1),
                        text_kwargs={'color': 'black','fontsize':16, 'alpha':0.7},
                        poly_kwargs={'facecolor': (0.5, 0.5, 0.5), 'alpha':0.5},#TODO: replace with purple
                        ax=ax)
    '''
    annotation.slope_marker(origin=(x1, y1),
                            slope=slope,
                            text_kwargs={'color': 'black','fontsize':16, 'alpha':0.7},
                            poly_kwargs={'facecolor': (0.5, 0.5, 0.5), 'alpha':0.5},#TODO: replace with purple
                            ax=ax)
    return True
