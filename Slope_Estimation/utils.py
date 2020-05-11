import matplotlib.pyplot as plt
import os
import pyproj
import math
from tqdm import tqdm
import pickle


def plot_lat_long_points(points):
    """
    Plot given lat long points
    Args:
        points (list): points
    """
    plt.scatter(x=[x[0] for x in points], y=[x[1] for x in points])
    plt.plot(points[0], points[-1])
    plt.show()


def gps_to_ecef_pyproj(lat_long_alt):
    """
    Convert gps lat long alt coordinates to ecef
    Args:
        lat_long_alt (list): lat, long, alt

    Returns:
        x, y, z: ecef coordinates

    """
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


# def get_bounding_box_coordinates(n, probe_dict, link_data):
#     """
#     Get bounding box for each zone of the map
#     Args:
#         n (int): Number of part to divide each side in to. For n=2, divide entire map into 4 parts (2x2).
#         probe_dict (dict): Dictionary of all probe points
#         link_data (dataframe): Pandas df of all link data
#
#     Returns:
#         coordinates dictionary for each zone number as key and it's bounding box coordinates as it values
#
#     """
#     # print(link_data.shapeInfo)
#     link_coordinates = []
#     for i, row in enumerate(tqdm(link_data.shapeInfo)):
#         points = [(x.split('/')) for x in row.split('|')]
#         link_coordinates.append(gps_to_ecef_pyproj(points[0][:2]))
#         link_coordinates.append(gps_to_ecef_pyproj(points[-1][:2]))
#     link_coordinates = np.array(link_coordinates)
#     x_max, y_max = np.amax(link_coordinates, axis=0)
#     x_min, y_min = np.amin(link_coordinates, axis=0)
#     print(x_min, y_min, x_max, y_max )
#     # x_interval = (x_max - x_min)/n
#     # y_interval = (y_max - y_min)/n
#     # coordinates_dict = {}
#     #
#     # for i in range(n):
#     #     coordinates_dict[i] = [x_min + x_interval*i]
#     return x_min, y_min, x_max, y_max


def slope_using_two_points(x1, x2, y1, y2):
    """
    Get slope using two point form
    Args:
        x1:
        x2:
        y1:
        y2:

    Returns:
        slope
    """
    try:
        return (float(y1) - float(y2)) / (float(x1) - float(x2))
    except ZeroDivisionError:
        return 99999


def slope_using_points_and_altitude(h1, h2, x1, y1, x2, y2):
    """
    Get slope using two points at given altitude
    Args:
        h1: alt 1
        h2: alt 2
        x1:
        y1:
        x2:
        y2:

    Returns:
        slope
    """
    if h1 != h2:
        sign = (h2 - h1) / abs(h2 - h1)
    else:
        sign = 1
    d = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)
    try:
        return sign * math.tan(math.asin(abs(h1 - h2) / d))
    except ZeroDivisionError:
        return sign * math.tan(math.asin(abs(h1 - h2) / 0.1))


def save_pickle(data, file):
    with open(file, 'wb') as f:
        pickle.dump(data, f)


def load_pickle(file):
    with open(file, 'rb') as f:
        data = pickle.load(f)
    return data


class Metadata:
    def __init__(self, n):
        """
        Metadata for location where the data comes from
        Args:
            n (int): number on grids per axis in which data is divided into
        """
        self.n = n
        self.x1, self.y1 = 3727482.4232750153, 5067892.186070938        # x_min, y_min
        self.x2, self.y2 = 4002608.377697181, 4837909.841133979         # x_max, y_max
        self.d_x = abs((self.x2 - self.x1) / n)
        self.d_y = abs((self.y1 - self.y2) / n)

