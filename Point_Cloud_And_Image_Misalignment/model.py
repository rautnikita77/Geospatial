import torch
from torch import nn
import cv2
from Point_Cloud_And_Image_Misalignment.utils import enu2cam, cam2image, lla2ecef, ecef2enu
import numpy as np
import pandas as pd
import os
from tqdm import tqdm


def create_image(points):
    img = torch.zeros((2048, 2048))
    for point in points:
        img[point[0], point[1]] = point[2]
    return img


class Model(nn.Module):

    def __init__(self, point_cloud_file, camera_config_file):
        super(Model, self).__init__()
        self.point_cloud = pd.read_csv(point_cloud_file, sep=' ', names=['lat', 'lon', 'alt', 'intensity'])
        self.camera_config = pd.read_csv(camera_config_file)
        self.camera_config.columns = ['lat', 'lon', 'alt', 'qs', 'qx', 'qy', 'qz']
        self.camera_config = self.camera_config.to_dict()
        for key, value in self.camera_config.items():
            self.camera_config[key] = nn.Parameter(torch.tensor(value[0]))
        print(self.camera_config)

    def forward(self):
        points_front, points_back, points_left, points_right = [], [], [], []
        for index, row in tqdm(self.point_cloud.iterrows()):

            x, y, z = lla2ecef(row.lat, row.lon, row.alt)
            e, n, u = ecef2enu(x, y, z, self.camera_config['lat'], self.camera_config['lon'],
                               self.camera_config['alt'])
            x, y, z = enu2cam(e, n, u, -self.camera_config['qs'], self.camera_config['qx'],
                              self.camera_config['qy'], self.camera_config['qz'])

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

        return front, back, left, right


if __name__ == "__main__":
    model = Model('/Users/anupamtripathi/PycharmProjects/Geospatial/Point_Cloud_And_Image_Misalignment/data/final_project_point_cloud.fuse',
                  '/Users/anupamtripathi/PycharmProjects/Geospatial/Point_Cloud_And_Image_Misalignment/data/image/camera.config')
    optimizer = torch.optim.Adam(list(model.camera_config.values()), lr=1)
    f, b, l, r = model()
    loss = torch.sum(f)
    print(model.camera_config)
    loss.backward()
    optimizer.step()
    print(model.camera_config)
