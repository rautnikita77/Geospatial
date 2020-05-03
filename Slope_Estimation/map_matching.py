import os
import math
import pandas as pd
from Slope_Estimation.utils import gps_to_ecef_pyproj
from tqdm import tqdm

data = 'probe_data_map_matching'

link_dict, probe_dict = {}, {}
err = 2


def find_candidate_points(link_data, probe_data):
    candidates = []
    for index, row in tqdm(link_data.iterrows()):
        link_dict[index] = {}
        link_dict[index]['toRefSpeedLimit'] = row.toRefSpeedLimit
        link_dict[index]['fromRefSpeedLimit'] = row.fromRefSpeedLimit
        link_dict[index]['toRefNumLanes'] = row.toRefNumLanes
        link_dict[index]['fromRefNumLanes'] = row.fromRefNumLanes
        link_dict[index]['Candidates'] = []
        points = [(x.split('/')) for x in row.shapeInfo.split('|')]
        # print(points)
        for i in tqdm(range(len(points)-1)):
            s = gps_to_ecef_pyproj(list(map(float, points[i][:2])))
            e = gps_to_ecef_pyproj(list(map(float, points[i + 1][:2])))
            theta = (s[1] - e[1]) / (s[0] - e[0])
            (d1, d2) = (int(link_dict[index]['toRefNumLanes'])*2, int(link_dict[index]['fromRefSpeedLimit'])*2)
            (x1, y1) = (s[0] + d1*math.sin(theta) + err, s[1] + d1*math.cos(theta) + err)
            (x2, y2) = (e[0] + d2*math.sin(theta) - err, e[1] + d2*math.cos(theta) - err)
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            link_dict[index]['co-ordinates'] = [s, e]
            for index1, probe in tqdm(probe_data.iterrows()):
                probe_dict[index1] = {}
                probe_dict[index1]['sampleID'] = probe.sampleID
                (x, y) = gps_to_ecef_pyproj([probe.latitude, probe.longitude])
                probe_dict[index1]['co-ordinates'] = (x, y)
                probe_dict[index1]['speed'] = probe.speed
                probe_dict[index1]['heading'] = probe.heading
                # print(probe_dict)
                if (x1 < x < x2) and (y1 < y < y2):
                    link_dict[index]['Candidates'].append(index1)
                # print(candidates)


    return candidates

def main():

    link_cols = ['linkPVID', 'fromRefSpeedLimit', 'toRefSpeedLimit', 'fromRefNumLanes', 'toRefNumLanes', 'shapeInfo']
    probe_cols = ['sampleID', 'latitude', 'longitude', 'altitude', 'speed', 'heading']
    link_header = ['linkPVID', 'refNodeID', 'nrefNodeID', 'length', 'functionalClass', 'directionOfTravel', 'speedCategory',
                   'fromRefSpeedLimit', 'toRefSpeedLimit', 'fromRefNumLanes', 'toRefNumLanes', 'multiDigitized', 'urban',
                   'timeZone', 'shapeInfo', 'curvatureInfo', 'slopeInfo']
    probe_header = ['sampleID', 'dateTime', 'sourceCode', 'latitude', 'longitude', 'altitude', 'speed', 'heading']
    link_data = pd.read_csv(os.path.join(data, 'Partition6467LinkData.csv'), names=link_header, usecols=link_cols,
                            index_col='linkPVID')
    probe_data = pd.read_csv(os.path.join(data, 'Partition6467ProbePoints.csv'), names=probe_header, usecols=probe_cols)

    candidates = find_candidate_points(link_data, probe_data)
    print(link_dict)



if __name__ == '__main__':
    main()
