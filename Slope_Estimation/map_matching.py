import os
import math
import random
import pandas as pd
from Slope_Estimation.utils import gps_to_ecef_pyproj, load_pickle, Metadata, delete_keys_dict, slope_using_two_points, slope_using_points_and_altitude
from Slope_Estimation.refine import refine_points
from tqdm import tqdm
import numpy as np
from sklearn.metrics import r2_score


data = 'data'

link_dict = {}

cov_constant = 1
err = 0 * cov_constant
lane_width = 3.75
n = 128             # Number of divisions for each axis


def find_candidate_points(link_data, probe_dict):
    global link_dict

    slope = []
    ground_truth = []
    germany = Metadata(n)
    flag = 0
    equ = lambda x, y, xp, yp, m: (yp - y) - m*(xp - x)
    pbar = tqdm(total=len(link_data.index))
    for index, row in link_data.iterrows():
        if row.slopeInfo != row.slopeInfo:
            pbar.update(1)
            continue
        link_slope = 0
        denominator = 0
        link_dict[index] = {}                   # {toRefSpeedLimit, fromRefSpeedLimit....., subLinks}
        link_dict[index]['toRefSpeedLimit'] = row.toRefSpeedLimit
        link_dict[index]['fromRefSpeedLimit'] = row.fromRefSpeedLimit
        link_dict[index]['toRefNumLanes'] = row.toRefNumLanes
        link_dict[index]['fromRefNumLanes'] = row.fromRefNumLanes
        link_dict[index]['subLinks'] = {}
        points = [(x.split('/')) for x in row.shapeInfo.split('|')]
        for point_idx in range(len(points)-1):          # for each sub-link
            sub_link_dict = {}                          # {co-ordinates, theta, candidates}
            s = gps_to_ecef_pyproj(list(map(float, points[point_idx][:2])))
            e = gps_to_ecef_pyproj(list(map(float, points[point_idx + 1][:2])))

            if e[1] > s[1]:
                s, e = e, s
            m = (s[1] - e[1]) / (s[0] - e[0])
            theta = math.atan(m)  # in radians

            (d1, d2) = (int(link_dict[index]['toRefNumLanes'] + 20)*lane_width, int(link_dict[index]['fromRefSpeedLimit'] + 20)*lane_width)

            (x1, y1) = (s[0] + d1*math.sin(theta)*cov_constant + (err*math.sin(theta)/abs(math.sin(theta))),
                        s[1] - d1*math.cos(theta)*cov_constant - (err*math.cos(theta)/abs(math.cos(theta))))
            (x2, y2) = (e[0] - d2*math.sin(theta)*cov_constant - (err*math.sin(theta)/abs(math.sin(theta))),
                        e[1] + d2*math.cos(theta)*cov_constant + (err*math.cos(theta)/abs(math.cos(theta))))

            i = (s[0] - germany.x1) // germany.d_x             # row number for nxn grid
            j = (s[1] - germany.y2) // germany.d_y             # col number for nxn grid
            zone = (n * j) + i
            sub_link_dict['zone'] = zone

            sub_link_dict['co-ordinates'] = [s, e]
            sub_link_dict['theta'] = theta
            sub_link_dict['candidates'] = []

            for index1, probe in probe_dict[zone].items():

                x, y = probe['co-ordinates']

                if equ(x1, y1, x, y, math.tan(theta)) >= 0 \
                        and equ(x1, y1, x, y, math.tan(math.atan(-1/m))) <= 0 \
                        and equ(x2, y2, x, y, math.tan(theta)) <= 0 \
                        and equ(x2, y2, x, y, math.tan(math.atan(-1/m))) >= 0:

                    sub_link_dict['candidates'].append(index1)

            if sub_link_dict['candidates']:
                sub_link_dict['candidates'] = refine_points(sub_link_dict, probe_dict[zone], link_dict[index])
            link_dict[index]['subLinks'][point_idx] = sub_link_dict

            slopes = []
            if len(sub_link_dict['candidates']) not in [0, 1]:
                for _ in range(5):
                    a, b = random.sample(list(sub_link_dict['candidates']), 2)
                    try:
                        slopes.append(slope_using_points_and_altitude(probe_dict[zone][a]['altitude'], probe_dict[zone][b]['altitude'],
                                            probe_dict[zone][a]['co-ordinates'][0], probe_dict[zone][a]['co-ordinates'][1],
                                            probe_dict[zone][b]['co-ordinates'][0], probe_dict[zone][b]['co-ordinates'][1]))
                    except ValueError:
                        pass
                [(x1, y1), (x2, y2)] = sub_link_dict['co-ordinates']
                if slopes:
                    link_slope += ((x1 - x2)**2 + (y1 - y2)**2)**(1/2) * sum(slopes) / len(slopes)
                    denominator += ((x1 - x2)**2 + (y1 - y2)**2)**(1/2)

            probe_dict[zone] = delete_keys_dict(probe_dict[zone], sub_link_dict['candidates'])
        if denominator != 0:
            link_dict[index]['slope'] = link_slope / denominator
            slope.append(link_dict[index]['slope'])
            ground_truth_link = [float(x.split('/')[1]) for x in row.slopeInfo.split('|')]
            ground_truth.append(sum(ground_truth_link) / len(ground_truth_link))
        pbar.update(1)
    pbar.close()
    print(r2_score(ground_truth, slope))
    return link_dict


def main():
    global link_dict, probe_dict
    link_cols = ['linkPVID', 'fromRefSpeedLimit', 'toRefSpeedLimit', 'fromRefNumLanes', 'toRefNumLanes', 'shapeInfo', 'slopeInfo']
    link_header = ['linkPVID', 'refNodeID', 'nrefNodeID', 'length', 'functionalClass', 'directionOfTravel', 'speedCategory',
                   'fromRefSpeedLimit', 'toRefSpeedLimit', 'fromRefNumLanes', 'toRefNumLanes', 'multiDigitized', 'urban',
                   'timeZone', 'shapeInfo', 'curvatureInfo', 'slopeInfo']
    link_data = pd.read_csv(os.path.join(data, 'Partition6467LinkData.csv'), names=link_header, usecols=link_cols,
                            index_col='linkPVID')

    probe_dict = load_pickle(os.path.join(data, 'probe_dict_128_zones_1000000_samples.pkl'))
    link_dict = find_candidate_points(link_data, probe_dict)



if __name__ == '__main__':
    main()
