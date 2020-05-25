import os
import numpy as np
import pandas as pd
import pymap3d as pm
from Point_Cloud_And_Image_Misalignment.utils import enu2cam, cam2image, lla2ecef, ecef2enu
import cv2
import matplotlib.pyplot as plt



root = 'data/'

# 45.887269, 11.040389, 247.614169, -0.696910, -0.675713, 0.172945, 0.166786

point_cloud = pd.read_csv(os.path.join(root, 'final_project_point_cloud.fuse'), sep=' ',
                          names = ['lat', 'lon', 'alt', 'intensity'])
camera_config = pd.read_csv(os.path.join(root, 'image', 'camera.config'))
camera_config.columns = ['lat', 'lon', 'alt', 'qs', 'qx', 'qy', 'qz']
print(camera_config)

points = []

for index, row in point_cloud.iterrows():

    x, y, z = lla2ecef(row.lat, row.lon, row.alt)
    e, n, u = ecef2enu(x, y, z, camera_config.lat.values[0], camera_config.lon.values[0], camera_config.alt.values[0])
    x, y, z = enu2cam(e, n, u, -camera_config.qs.values[0], camera_config.qx.values[0], camera_config.qy.values[0], camera_config.qz.values[0])

    a = cam2image(x, y, z, 1024)
    if a == None:
        continue
    else:
        points.append([int(a[0]), int(a[1]), int(row.intensity)])



img = np.zeros((2048, 2048))
for point in points:
    img[point[0], point[1]] = point[2]


# plt.imshow(img)
# plt.show()
cv2.imshow("a",img)
cv2.waitKey(0)
cv2.imwrite("front.jpg", img)




