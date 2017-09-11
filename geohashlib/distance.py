# -*- coding: utf-8 -*-
"""Distance functions

Vectorized (numpy happy) implementations of haversine or euclidean (approx) distance

Todo:
    * Add euclidean and come up with avg distance per degree
"""
import numpy as np

def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

# def euclidean_np(lon1, lat1, lon2, lat2):
#     """
#     :param lon1:
#     :param lat1:
#     :param lon2:
#     :param lat2:
#     :return:
#     """
#
#     # Calculate avg lat/lon length for a degree for the range given
#     lon_length=0
#     lat_length=0
#     lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
#
#     dlon = lon2 - lon1
#     dlat = lat2 - lat1
#     c_squared = (dlon * lon_length ) **2 + (dlat * lat_length)**2
#     c = np.sqrt(c_squared)
