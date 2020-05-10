import os
import pandas as pd
from Slope_Estimation.utils import gps_to_ecef_pyproj, slope_using_two_points
from tqdm import tqdm


def partition_probe(probe_dict):
    n = 8
    # coordinates = get_bounding_box_coordinates(n, probe_dict, link_data)
    probe_dicts = {x: [] for x in range(n*n)}

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
        probe['zone'] = dict_index
        probe_dicts[dict_index].append(probe)

    sum_ = 0
    for x, y in probe_dicts.items():
        sum_ += len(y)
        print(x, len(y))
    print('Number of probe points partitioned = ', sum_)
    return probe_dicts


def partition_link(link_data):
    n = 8
    x1, y1 = gps_to_ecef_pyproj([54.898068, 5.748880])
    x2, y2 = gps_to_ecef_pyproj([47.441747, 15.623851])
    dx = abs((x2 - x1) / n)
    dy = abs((y1 - y2) / n)

    link_dicts = {x: [] for x in range(n*n)}

    for index, row in tqdm(link_data.iterrows()):
        to_flaot = lambda x: float(x) if x else -1
        points = [list(map(to_flaot, x.split('/'))) for x in row.shapeInfo.split('|')]
        print(points)
        points = [points[0][0:2], points[1][0:2]]
        points = list(map(gps_to_ecef_pyproj, points))
        link = row.to_dict()
        x, y = points[0]

        i = (x - x1) // dx
        j = (y - y2) // dy
        dict_index = (n * j) + i
        link['zone'] = dict_index
        # link['points']
        print(link)
        break
        # link_dicts[dict_index].append(probe)


if __name__ == "__main__":
    data = 'data'
    link_cols = ['linkPVID', 'fromRefSpeedLimit', 'toRefSpeedLimit', 'fromRefNumLanes', 'toRefNumLanes', 'shapeInfo']
    # probe_cols = ['sampleID', 'latitude', 'longitude', 'altitude', 'speed', 'heading']
    link_header = ['linkPVID', 'refNodeID', 'nrefNodeID', 'length', 'functionalClass', 'directionOfTravel', 'speedCategory',
                   'fromRefSpeedLimit', 'toRefSpeedLimit', 'fromRefNumLanes', 'toRefNumLanes', 'multiDigitized', 'urban',
                   'timeZone', 'shapeInfo', 'curvatureInfo', 'slopeInfo']
    # probe_header = ['sampleID', 'dateTime', 'sourceCode', 'latitude', 'longitude', 'altitude', 'speed', 'heading']
    link_data = pd.read_csv(os.path.join(data, 'Partition6467LinkData.csv'), names=link_header, usecols=link_cols,
                            index_col='linkPVID')
    # probe_data = pd.read_csv(os.path.join(data, 'Partition6467ProbePoints.csv'), names=probe_header, usecols=probe_cols)

    # probe_dict = probe_data.sample(n=100000).to_dict('index')
    link_dataframe = partition_link(link_data)
    # probe_dicts = partition_probe(probe_dict, [])
