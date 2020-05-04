from Slope_Estimation.utils import gps_to_ecef_pyproj
import numpy as np


def refine_points(sub_link_dict, probe_dict, link_dict):
    """
    Refines the candidate points for a given sub link
    Args:
        sub_link_dict (dict): Sub link dictionary
        probe_dict (dict): Probe data dictionary
        link_dict (dict): Link data dictionary

    Returns:
        refined_points (ndarray): List of refined points
    """

    candidate_points = sub_link_dict['candidates']

    points_to_remove = []
    candidate_type_count = {}
    total_probes = 0
    for n, p in enumerate(candidate_points):
        speed_probe = probe_dict[p]['speed'] % 180
        slope_link = sub_link_dict['theta']
        slope_probe = probe_dict[p]['heading']
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
            direction = 'to'
        else:
            direction = 'from'
        speed_link = link_dict[direction + 'RefSpeedLimit']
        if speed_probe > speed_link + 10 or speed_probe < speed_link - 40:      # Remove if speed is too high or too low
            points_to_remove.append(n)
        else:
            total_probes += 1
            try:
                candidate_type_count[probe_dict[p]['sampleID']] += 1
            except KeyError:
                candidate_type_count[probe_dict[p]['sampleID']] = 1

    candidate_points = np.delete(candidate_points, points_to_remove)
    threshold = np.quantile(np.array(list(candidate_type_count.values())), 0.75) / 2

    points_to_remove = []
    for p in candidate_points:
        if candidate_type_count[probe_dict[p]['sampleID']] < threshold:
            points_to_remove.append(p)
    candidate_points = np.delete(candidate_points, points_to_remove)

    return candidate_points


# if __name__ == "__main__":
#     link_dict = {0: {'theta': 30, 'To_speed': 40, 'From_speed': 50}}
#     probe_dict = {0: {'direction': 30, 'speed': 45, 'device': 10},
#                   1: {'direction': 320, 'speed': 30, 'device': 0},
#                   2: {'direction': 320, 'speed': 130, 'device': 0},
#                   3: {'direction': 320, 'speed': 30, 'device': 20},
#                   4: {'direction': 320, 'speed': 30, 'device': 10},
#                   5: {'direction': 320, 'speed': 30, 'device': 10}
#                   }
#     print(refine_points(0, [0, 1, 2, 3, 4, 5]))
