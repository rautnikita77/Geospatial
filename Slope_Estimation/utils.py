import matplotlib.pyplot as plt
import os
import pyproj
import pandas as pd
from tqdm import tqdm
import pickle
# 3727482.4232750153 4837909.841133979 4002608.377697181 5067892.186070938 = x_min, y_min, x_max, y_max

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
    return (y1 - y2) / (x1 - x2)


def save_pickle(data, file):
    with open(file, 'wb') as f:
        pickle.dump(data, f)

# if __name__ == "__main__":
#     data = 'data'
#     link_cols = ['linkPVID', 'fromRefSpeedLimit', 'toRefSpeedLimit', 'fromRefNumLanes', 'toRefNumLanes', 'shapeInfo']
#     probe_cols = ['sampleID', 'latitude', 'longitude', 'altitude', 'speed', 'heading']
#     link_header = ['linkPVID', 'refNodeID', 'nrefNodeID', 'length', 'functionalClass', 'directionOfTravel',
#                    'speedCategory',
#                    'fromRefSpeedLimit', 'toRefSpeedLimit', 'fromRefNumLanes', 'toRefNumLanes', 'multiDigitized',
#                    'urban',
#                    'timeZone', 'shapeInfo', 'curvatureInfo', 'slopeInfo']
#     probe_header = ['sampleID', 'dateTime', 'sourceCode', 'latitude', 'longitude', 'altitude', 'speed', 'heading']
#     link_data = pd.read_csv(os.path.join(data, 'Partition6467LinkData.csv'), names=link_header, usecols=link_cols,
#                             index_col='linkPVID')
#     probe_data = pd.read_csv(os.path.join(data, 'Partition6467ProbePoints.csv'), names=probe_header, usecols=probe_cols)
#
#     probe_dict = probe_data.sample(n=100).to_dict('index')
#     get_bounding_box_coordinates(4, probe_dict, link_data)
