from Slope_Estimation.utils import gps_to_ecef_pyproj
import numpy as np


def refine_points(link_id, candidate_points):
    """
    Refines the candidate points
    Args:
        link_id (int): Identifier for link
        candidate_points (ndarray): List of candidate point keys

    Returns:
        refined_points (ndarray): List of refined points
    """
    global link_dict, probe_dict

    points_to_remove = []
    candidate_type_count = {}
    total_probes = 0
    for n, p in enumerate(candidate_points):
        speed_probe = probe_dict[p]['speed'] % 180
        slope_link = link_dict[link_id]['theta']
        slope_probe = probe_dict[p]['direction']
        # if abs(abs(slope_link) - slope_probe) >= 90:
        #     if slope_link >= 0:
        #         direction = 'To'
        #     else:
        #         direction = 'From'
        # else:
        #     if slope_link >= 0:
        #         direction = 'From'
        #     else:
        #         direction = 'To'
        if abs(slope_link - slope_probe) >= 90:
            direction = 'To'
        else:
            direction = 'From'
        speed_link = link_dict[link_id][direction + '_speed']
        if speed_probe > speed_link + 10 or speed_probe < speed_link - 40:      # Remove if speed is too high or too low
            points_to_remove.append(n)
        else:
            total_probes += 1
            try:
                candidate_type_count[probe_dict[p]['device']] += 1
            except KeyError:
                candidate_type_count[probe_dict[p]['device']] = 1

    candidate_points = np.delete(candidate_points, points_to_remove)

    threshold = np.quantile(np.array(list(candidate_type_count.values())), 0.75) / 2

    points_to_remove = []
    for p in candidate_points:
        if candidate_type_count[probe_dict[p]['device']] < threshold:
            points_to_remove.append(p)
    candidate_points = np.delete(candidate_points, points_to_remove)

    return candidate_points


if __name__ == "__main__":
    link_dict = {0: {'theta': 30, 'To_speed': 40, 'From_speed': 50}}
    probe_dict = {0: {'direction': 30, 'speed': 45, 'device': 10},
                  1: {'direction': 320, 'speed': 30, 'device': 0},
                  2: {'direction': 320, 'speed': 130, 'device': 0},
                  3: {'direction': 320, 'speed': 30, 'device': 20},
                  4: {'direction': 320, 'speed': 30, 'device': 10},
                  5: {'direction': 320, 'speed': 30, 'device': 10}
                  }
    print(refine_points(0, [0, 1, 2, 3, 4, 5]))
