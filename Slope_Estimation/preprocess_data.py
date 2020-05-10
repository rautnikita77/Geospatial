import os
import pandas as pd
from Slope_Estimation.utils import gps_to_ecef_pyproj
from tqdm import tqdm


def partition_data(probe_dict, link_data):
    n = 8
    # coordinates = get_bounding_box_coordinates(n, probe_dict, link_data)
    probe_dicts, link_dataframes = {x: [] for x in range(n*n)}, []

    # (x1, y1), (x2, y2) = coordinates
    x1, y1 = gps_to_ecef_pyproj([54.898068, 5.748880])
    x2, y2 = gps_to_ecef_pyproj([47.441747, 15.623851])
    dx = abs((x2 - x1) / n)
    dy = abs((y1 - y2) / n)

    for key, probe in tqdm(probe_dict.items()):
        x, y = gps_to_ecef_pyproj([probe['latitude'], probe['longitude']])
        i = (x - x1) // dx
        j = (y - y2) // dy
        dict_index = (n * j) + i
        probe_dicts[dict_index].append(probe)

    sum_ = 0
    for x, y in probe_dicts.items():
        sum_ += len(y)
        print(x, len(y))

    print(sum_)


if __name__ == "__main__":
    data = 'data'
    # link_cols = ['linkPVID', 'fromRefSpeedLimit', 'toRefSpeedLimit', 'fromRefNumLanes', 'toRefNumLanes', 'shapeInfo']
    probe_cols = ['sampleID', 'latitude', 'longitude', 'altitude', 'speed', 'heading']
    # link_header = ['linkPVID', 'refNodeID', 'nrefNodeID', 'length', 'functionalClass', 'directionOfTravel', 'speedCategory',
    #                'fromRefSpeedLimit', 'toRefSpeedLimit', 'fromRefNumLanes', 'toRefNumLanes', 'multiDigitized', 'urban',
    #                'timeZone', 'shapeInfo', 'curvatureInfo', 'slopeInfo']
    probe_header = ['sampleID', 'dateTime', 'sourceCode', 'latitude', 'longitude', 'altitude', 'speed', 'heading']
    # link_data = pd.read_csv(os.path.join(data, 'Partition6467LinkData.csv'), names=link_header, usecols=link_cols,
    #                         index_col='linkPVID')
    probe_data = pd.read_csv(os.path.join(data, 'Partition6467ProbePoints.csv'), names=probe_header, usecols=probe_cols)

    probe_dict = probe_data.sample(n=100000).to_dict('index')
    partition_data(probe_dict, [])
