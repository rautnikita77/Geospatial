import numpy as np
from Slope_Estimation.utils import delete_keys_dict


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
        speed_probe = probe_dict[p]['speed']
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
        orientation = 1 if sub_link_dict['co-ordinates'][0][1] < sub_link_dict['co-ordinates'][1][1] else -1
        if abs(slope_link - slope_probe) >= 90:
            direction = 'to' if orientation == 1 else 'from'
        else:
            direction = 'from' if orientation == 1 else 'to'
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

    probe_dict = delete_keys_dict(probe_dict, candidate_points)

    return candidate_points, probe_dict


if __name__ == "__main__":
    link_dict = {0: {'toRefSpeedLimit': 40, 'fromRefSpeedLimit': 50}}
    probe_dict = {0: {'heading': 30, 'speed': 45, 'sampleID': 10},
                  1: {'heading': 90, 'speed': 30, 'sampleID': 0},
                  2: {'heading': 136, 'speed': 130, 'sampleID': 0},
                  3: {'heading': 150, 'speed': 30, 'sampleID': 20},
                  4: {'heading': 180, 'speed': 30, 'sampleID': 10},
                  5: {'heading': 320, 'speed': 30, 'sampleID': 10}
                  }
    sub_link_dict = {'co-ordinates': [(0, 0), (1, 1)], 'theta': 45, 'candidates': [0, 1, 2, 3, 4, 5]}
    print(refine_points(sub_link_dict, probe_dict, link_dict[0]))
