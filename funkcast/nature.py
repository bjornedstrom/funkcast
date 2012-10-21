# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Björn Edström <be@bjrn.se>
# See license for details.

"""The purpose of this module is to take a weather data point (such as
air pressure  or wind  direction) and normalize it to a scalar value
[0.0,1.0] and a distrubution.
"""

import math


# TODO (bjorn): Rename this.
# TODO (bjorn): Return distribution.
def normalize(data_type, series, scalar, absolute):
    """Normalize nature data.

       data_type: string describing the data (such as
         "wind-direction")
       series: a list with all available data points.
       scalar: the data point to normalize.
       absolute: true to normalize absolutely.
    """

    length = max(series) - min(series)
    shifted = scalar - min(series)
    norm = shifted / length

    if data_type == 'wind-direction':
        if absolute:
            norm = scalar / 360.0
    elif data_type == 'wind-speed': # XXX
        if absolute:
            norm = scalar / 20.0
    elif data_type == 'temperature': # XXX
        if absolute:
            # -20 to 40
            temp = max(0, scalar + 20)
            # 0 to 60
            norm =  temp / 60.0
    elif data_type == 'pressure':
        # world records are low 870 and high 1085.7
        # standard atmosphere = 1013
        if absolute:
            norm = (scalar - 980) / 1040 # XXX
            if norm < 0:
                norm = 0
            elif norm > 1.0:
                norm = 1.0
    elif data_type == 'cloud-cover':
        if absolute:
            norm = scalar / 3.0
    elif data_type == 'rain':
        if absolute:
            norm = min(1.0, scalar / 10.0) # XXX

    return norm
