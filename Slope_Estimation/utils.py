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


def delete_keys_dict(dict_, keys):
    """
    Delete multiple keys from a dictionary
    Args:
        dict_ (dict): Dictionary in which keys need to be removed
        keys (ndarray): List of keys to be removed

    Returns:
        dict_ with removed keys
    """
    for k in keys:
        del dict_[k]
    return dict_


def get_bounding_box_coordinates(probe_dict, link_data):
    """
    Get bounding box for each zone of the map
    Args:
        probe_dict (dict): Dictionary of all probe points
        link_data (dataframe): Pandas df of all link data

    Returns:
        coordinates dictionary for each zone number as key and it's bounding box coordinates as it values

    """
    pass
