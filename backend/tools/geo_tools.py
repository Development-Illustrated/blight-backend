import numpy as np
from math import sin, cos, sqrt, atan2
import geopy.distance


# Check bject is within range of other object
def within_range(alat, alng, blat, blng, range):
    if calc_distance(alat, alng, blat, blng) < range:
        return True
    else:
        return False

def calc_distance(alat, alng, blat, blng):

    coords_1 = (alat, alng)
    coords_2 = (blat, blng)
    return geopy.distance.vincenty(coords_1, coords_2).km


