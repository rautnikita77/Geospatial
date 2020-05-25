import os
import numpy as np
import pandas as pd
from Point_Cloud_And_Image_Misalignment.utils import enu2cam, cam2image, lla2ecef, ecef2enu
import cv2
import matplotlib.pyplot as plt



root = 'data/'


point_cloud = pd.read_csv(os.path.join(root, 'final_project_point_cloud.fuse'), sep=' ',
                          names = ['lat', 'lon', 'alt', 'intensity'])
camera_config = pd.read_csv(os.path.join(root, 'image', 'camera.config'))
camera_config.columns = ['lat', 'lon', 'alt', 'qs', 'qx', 'qy', 'qz']
print(camera_config)

points_front, points_back, points_left, points_right = [], [], [], []

for index, row in point_cloud.iterrows():

    x, y, z = lla2ecef(row.lat, row.lon, row.alt)
    e, n, u = ecef2enu(x, y, z, camera_config.lat.values[0], camera_config.lon.values[0], camera_config.alt.values[0])
    x, y, z = enu2cam(e, n, u, -camera_config.qs.values[0], camera_config.qx.values[0], camera_config.qy.values[0], camera_config.qz.values[0])


    if z > 0 and z > abs(x) and z > abs(y):
        front = cam2image(x, y, z, 1024)
        points_front.append([int(front[0]), int(front[1]), int(row.intensity)])

    if z < 0 and z > abs(x) and z > abs(y):
        back = cam2image(x, y, z, 1024)
        points_back.append([int(back[0]), int(back[1]), int(row.intensity)])



front = np.zeros((2048, 2048))
for point in points_front:
    front[point[0], point[1]] = point[2]

back = np.zeros((2048, 2048))
for point in points_back:
    back[point[0], point[1]] = point[2]


# plt.imshow(img)
# plt.show()
cv2.imshow("a",front)
cv2.waitKey(0)
cv2.imshow("a",back)
cv2.waitKey(0)
# cv2.imwrite("front.jpg", img)




