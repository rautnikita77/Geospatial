import os
import numpy as np
import pandas as pd
from Point_Cloud_And_Image_Misalignment.utils import enu2cam, cam2image, lla2ecef, ecef2enu
import cv2

root = 'data/'


def create_image(points):
    img = np.zeros((2048, 2048))
    for point in points:
        img[point[0], point[1]] = point[2]
    print(img)
    return img


def main():
    point_cloud = pd.read_csv(os.path.join(root, 'final_project_point_cloud.fuse'), sep=' ',
                              names=['lat', 'lon', 'alt', 'intensity'])
    camera_config = pd.read_csv(os.path.join(root, 'image', 'camera.config'))
    camera_config.columns = ['lat', 'lon', 'alt', 'qs', 'qx', 'qy', 'qz']

    points_front, points_back, points_left, points_right = [], [], [], []

    for index, row in point_cloud.iterrows():

        x, y, z = lla2ecef(row.lat, row.lon, row.alt)
        e, n, u = ecef2enu(x, y, z, camera_config.lat.values[0], camera_config.lon.values[0],
                           camera_config.alt.values[0])
        x, y, z = enu2cam(e, n, u, -camera_config.qs.values[0], camera_config.qx.values[0], camera_config.qy.values[0],
                          camera_config.qz.values[0])

        # Front Projection
        if z > 0 and z > abs(x) and z > abs(y):
            [x, y] = cam2image(x, y, z, 2048)
            points_front.append([int(x), int(y), int(row.intensity)])

        # Back Projection
        if z < 0 and -z > abs(x) and -z > abs(y):
            [x, y] = cam2image(x, -y, z, 2048)
            points_back.append([int(x), int(y), int(row.intensity)])

        # Left Projection
        if x > 0 and x > abs(z) and x > abs(y):
            [x, y] = cam2image(-z, y, x, 2048)
            points_right.append([int(x), int(y), int(row.intensity)])

        # Right Projection
        if x < 0 and -x > abs(z) and -x > abs(y):
            [x, y] = cam2image(z, y, -x, 2048)
            points_left.append([int(x), int(y), int(row.intensity)])

    front = create_image(points_front)
    back = create_image(points_back)
    left = create_image(points_left)
    right = create_image(points_right)

    cv2.imwrite(os.path.join(root, "projections/front.jpg"), front)
    cv2.imwrite(os.path.join(root, "projections/back.jpg"), back)
    cv2.imwrite(os.path.join(root, "projections/left.jpg"), left)
    cv2.imwrite(os.path.join(root, "projections/right.jpg"), right)


if __name__ == "__main__":
    main()




