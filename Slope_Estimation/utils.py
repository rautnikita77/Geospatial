import matplotlib.pyplot as plt
import numpy as np
import os
import pyproj


def plot_lat_long_points(points):
    # for lat, long in points:
    print(points)
    plt.scatter(x=[x[0] for x in points], y=[x[1] for x in points])
    plt.plot(points[0], points[-1])
    plt.show()


def gps_to_ecef_pyproj(lat_long_alt):

    if len(lat_long_alt) == 3:
        ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
        lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
        x, y, z = pyproj.transform(lla, ecef, lat_long_alt[0], lat_long_alt[1], lat_long_alt[2], radians=False)
        return (x, y, z)
    else:
        ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
        lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
        x, y = pyproj.transform(lla, ecef, lat_long_alt[0], lat_long_alt[1], radians=False)
        return (x, y)





print(gps_to_ecef_pyproj([2,2]))