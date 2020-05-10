import os
import math
import random
import pandas as pd
from Slope_Estimation.utils import gps_to_ecef_pyproj
from Slope_Estimation.refine import refine_points
from tqdm import tqdm


data = 'data'

link_dict, probe_dict = {}, {}

cov_constant = 1
err = 0 * cov_constant


def find_candidate_points(link_data):
    global link_dict, probe_dict

    candidates = []
    flag = 0
    equ = lambda x, y, xp, yp, m: (yp - y) - m*(xp - x)
    alt = lambda h1, h2, x1, y1, x2, y2: math.tan(math.degrees(math.asin(math.radians(abs(h1-h2)/((x1 - x2)**2 + (y1-y2)**2)**(1/2)))))
    for index, row in (link_data.iterrows()):
        link_slope = 0
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
            s = (2, 1)
            e = (1, 2)
            m = (s[1] - e[1]) / (s[0] - e[0])
            theta = math.atan(m)  # in radians

            print(m)
            print(theta)

            # print(link_dict[index]['toRefNumLanes'], link_dict[index]['fromRefSpeedLimit'])
            (d1, d2) = (int(link_dict[index]['toRefNumLanes'] + 20)*2, int(link_dict[index]['fromRefSpeedLimit'] + 20)*2)
            (d1, d2) = (1,1)
            # print(math.sin(math.radians(theta)))
            (x1, y1) = (s[0] + d1*math.sin(theta)*cov_constant + (err*math.sin(theta)/abs(math.sin(theta))),
                        s[1] - d1*math.cos(theta)*cov_constant - (err*math.cos(theta)/abs(math.cos(theta))))
            (x2, y2) = (e[0] - d2*math.sin(theta)*cov_constant - (err*math.sin(theta)/abs(math.sin(theta))),
                        e[1] + d2*math.cos(theta)*cov_constant + (err*math.cos(theta)/abs(math.cos(theta))))

            print(x1, y1, x2, y2)

            sub_link_dict['co-ordinates'] = [s, e]       # will overwrite each time
            sub_link_dict['theta'] = theta
            sub_link_dict['candidates'] = []
            # print(sub_link_dict['co-ordinates'])
            for index1, probe in tqdm(probe_dict.items()):

                (x, y, z) = gps_to_ecef_pyproj([probe['latitude'], probe['longitude'], probe['altitude']])
                x = (s[0] + e[0])/2
                y = (s[1] + e[1])/2

                if flag == 0:
                    probe_dict[index1]['co-ordinates'] = (x, y)
                    probe_dict[index1]['altitude'] = z

                if equ(x1, y1, x, y, math.tan(theta)) >= 0 \
                        and equ(x1, y1, x, y, math.tan(math.atan(-1/m))) <= 0 \
                        and equ(x2, y2, x, y, math.tan(theta)) <= 0 \
                        and equ(x2, y2, x, y, math.tan(math.atan(-1/m))) >= 0:
                    # print('a')
                    sub_link_dict['candidates'].append(index1)
            flag = 1
            print('candidates', len(sub_link_dict['candidates']))
            if sub_link_dict['candidates']:
                sub_link_dict['candidates'], probe_dict = refine_points(sub_link_dict, probe_dict, link_dict[index])
            link_dict[index]['subLinks'][i] = sub_link_dict

            altitude = []
            if len(sub_link_dict['candidates']) not in [0, 1]:
                for j in range(5):
                    a, b = random.sample(sub_link_dict['candidates'], 2)

                    altitude.append(alt(probe_dict[a]['altitude'], probe_dict[b]['altitude'],
                                        probe_dict[a]['co-ordinates'][0], probe_dict[a]['co-ordinates'][1],
                                        probe_dict[b]['co-ordinates'][0], probe_dict[b]['co-ordinates'][1]))

                [(x1, y1), (x2, y2)] = sub_link_dict['co-ordinates']
                link_slope += ((x1 - x2)**2 + (y1 - y2)**2)**(1/2) * sum(altitude) / len(altitude)

            else:
                link_slope += -1
            print(sub_link_dict['candidates'])
        link_dict[index]['slope'] = link_slope

    return candidates, link_dict


def partition_data(probe_dict, link_data):
    n = 2
    coordinates = get_bounding_box_coordinates(n, probe_dict, link_data)
    probe_dicts, link_dataframes = {x: [] for x in range(n*n)}, []

    (x1, y1), (x2, y2) = coordinates
    x1, y1 = 53.207633, 7.215272
    x2, y2 = 47.727688, 15.064739
    dx = abs((x2 - x1) / n)
    dy = abs((y1 - y2) / n)

    for n, probe in probe_dict:
        x, y = gps_to_ecef_pyproj([probe['latitude'], probe_dict['longitude']])

        i = (x - x1) // dx
        j = (y - y2) // dy

        dict_index = (n * j) + i

        probe_dicts[dict_index].append(probe)

    # for zone, coordinates in bounding_box_dict.items():
    #     (x1, y1), (x2, y2) = coordinates


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

    # probe_dict = probe_data.sample(n=1000).to_dict('index')
    probe_dict = probe_data[:1000].to_dict('index')
    # Create 16 parts of data. One probe_dict and one link_data dataframe for each part
    # For each part
    # find_candidate_points(probe_dict[i], link_data[i])

    # probe_dicts, link_dataframes = partition_data(probe_dict, link_data)
    # print(link_data)
    candidates, link_dict = find_candidate_points(link_data.iloc[0:1])


if __name__ == '__main__':
    main()
