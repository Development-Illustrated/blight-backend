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


print(within_range(51.4812333,-3.1770008,51.47461486888,-3.18987971215, 1.2))