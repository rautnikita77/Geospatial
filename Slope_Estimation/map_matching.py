import os
import math
import pandas as pd
from Slope_Estimation.utils import gps_to_ecef_pyproj
from Slope_Estimation.refine import refine_points
from tqdm import tqdm

data = 'data'

link_dict, probe_dict = {}, {}
cov_constant = 1.165 / 100
err = 2 * cov_constant



def find_candidate_points(link_data, probe_data):
    global link_dict, probe_dict
    candidates = []
    for index, row in tqdm(link_data.iterrows()):
        link_dict[index] = {}                   # {toRefSpeedLimit, fromRefSpeedLimit....., subLinks}
        link_dict[index]['toRefSpeedLimit'] = row.toRefSpeedLimit
        link_dict[index]['fromRefSpeedLimit'] = row.fromRefSpeedLimit
        link_dict[index]['toRefNumLanes'] = row.toRefNumLanes
        link_dict[index]['fromRefNumLanes'] = row.fromRefNumLanes
        link_dict[index]['subLinks'] = {}
        points = [(x.split('/')) for x in row.shapeInfo.split('|')]
        # print(points)
        for i in range(len(points)-1):          # for each sub-link
            sub_link_dict = {}                  # {co-ordinates, theta, candidates}
            s = gps_to_ecef_pyproj(list(map(float, points[i][:2])))
            e = gps_to_ecef_pyproj(list(map(float, points[i + 1][:2])))
            theta = (s[1] - e[1]) / (s[0] - e[0])
            (d1, d2) = (int(link_dict[index]['toRefNumLanes'])*2, int(link_dict[index]['fromRefSpeedLimit'])*2)
            (x1, y1) = (s[0] + d1*math.sin(theta)*cov_constant + err, s[1] + d1*math.cos(theta)*cov_constant + err)
            (x2, y2) = (e[0] + d2*math.sin(theta) - err, e[1] + d2*math.cos(theta) - err)
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            sub_link_dict['co-ordinates'] = [s, e]       # will overwrite each time
            sub_link_dict['theta'] = theta
            sub_link_dict['candidates'] = []
            for index1, probe in tqdm(probe_dict.items()):
                (x, y) = gps_to_ecef_pyproj([probe['latitude'], probe['longitude']])
                probe_dict[index1]['co-ordinates'] = (x, y)
                if (x1 < x < x2) and (y1 < y < y2):
                    sub_link_dict['candidates'].append(index1)
            link_dict[index]['subLinks'][i] = sub_link_dict
    print(link_dict)
    return candidates


def main():
    global link_dict, probe_dict
    link_cols = ['linkPVID', 'fromRefSpeedLimit', 'toRefSpeedLimit', 'fromRefNumLanes', 'toRefNumLanes', 'shapeInfo']
    probe_cols = ['sampleID', 'latitude', 'longitude', 'altitude', 'speed', 'heading']
    link_header = ['linkPVID', 'refNodeID', 'nrefNodeID', 'length', 'functionalClass', 'directionOfTravel', 'speedCategory',
                   'fromRefSpeedLimit', 'toRefSpeedLimit', 'fromRefNumLanes', 'toRefNumLanes', 'multiDigitized', 'urban',
                   'timeZone', 'shapeInfo', 'curvatureInfo', 'slopeInfo']
    probe_header = ['sampleID', 'dateTime', 'sourceCode', 'latitude', 'longitude', 'altitude', 'speed', 'heading']
    link_data = pd.read_csv(os.path.join(data, 'Partition6467LinkData.csv'), names=link_header, usecols=link_cols,
                            index_col='linkPVID')
    probe_data = pd.read_csv(os.path.join(data, 'Partition6467ProbePoints.csv'), names=probe_header, usecols=probe_cols)
    probe_dict = probe_data.iloc[0:10].to_dict('index')
    candidates = find_candidate_points(link_data.iloc[0:10], probe_data.iloc[0:10])
    # print(candidates)


if __name__ == '__main__':
    main()
