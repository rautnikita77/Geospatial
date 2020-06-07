import torch
from torch import nn
import cv2
from Point_Cloud_And_Image_Misalignment.utils import zoom_out, zoom_out_torch
import numpy as np
import pandas as pd
import os
from tqdm import tqdm
import numpy as np
import torch.nn.functional as F
from kornia.geometry.transform import warp_affine, crop_and_resize

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def create_image(points):
    img = torch.zeros((2048, 2048))
    for point in points:
        img[point[0], point[1]] = point[2]

    # print(img)
    return img


class Model(nn.Module):

    def __init__(self, rows, cols):
        super(Model, self).__init__()

        self.rows = rows
        self.cols = cols
        self.M_tune = torch.tensor([[1., 0., 0.], [0., 1., 0.]], requires_grad=True)

        self.boxes = torch.tensor([[[0., 0.],[2048., 0.],[2048., 2048.],[0., 2048.]]])
        self.k = 50
        self.n = nn.Parameter(torch.Tensor([self.k]))

    def forward(self, front_proj, back_proj, left_proj, right_proj):

        # print(self.M)
        self.M_fixed = torch.tensor([[1., 0., 0.], [0., 1., 0.]], requires_grad=False)

        mask = torch.tensor([[0, 0, 1], [0, 0, 1]], requires_grad=False)  # how to combine the two
        self.M = (mask * self.M_tune + (1 - mask) * self.M_fixed).unsqueeze(0)

        front_proj = warp_affine(front_proj, self.M, (self.cols, self.rows))
        back_proj = warp_affine(back_proj, self.M, (self.cols, self.rows))
        left_proj = warp_affine(left_proj, self.M, (self.cols, self.rows))
        right_proj = warp_affine(right_proj, self.M, (self.cols, self.rows))


        front_proj_outside = torch.zeros_like(front_proj)
        front_proj = crop_and_resize(front_proj, boxes=self.boxes, size=(self.rows - self.k, self.cols - self.k))
        front_proj = front_proj + self.n - self.n
        front_proj_outside[:, :, int(self.rows / 2) - int(front_proj.shape[2] / 2): int(self.rows / 2) + int(
            front_proj.shape[2] / 2), int(self.rows / 2) - int(front_proj.shape[2] / 2): int(self.rows / 2) + int(
            front_proj.shape[2] / 2)] = front_proj

        back_proj_outside = torch.zeros_like(back_proj)
        back_proj = crop_and_resize(back_proj, boxes=self.boxes, size=(self.rows - self.k, self.cols - self.k))
        back_proj = back_proj + self.n - self.n
        back_proj_outside[:, :, int(self.rows / 2) - int(back_proj.shape[2] / 2): int(self.rows / 2) + int(
            back_proj.shape[2] / 2), int(self.rows / 2) - int(back_proj.shape[2] / 2): int(self.rows / 2) + int(
            back_proj.shape[2] / 2)] = back_proj

        left_proj_outside = torch.zeros_like(left_proj)
        left_proj = crop_and_resize(left_proj, boxes=self.boxes, size=(self.rows - self.k, self.cols - self.k))
        left_proj = left_proj + self.n - self.n
        left_proj_outside[:, :, int(self.rows / 2) - int(left_proj.shape[2] / 2): int(self.rows / 2) + int(
            left_proj.shape[2] / 2), int(self.rows / 2) - int(left_proj.shape[2] / 2): int(self.rows / 2) + int(
            left_proj.shape[2] / 2)] = left_proj

        right_proj_outside = torch.zeros_like(right_proj)
        right_proj = crop_and_resize(right_proj, boxes=self.boxes, size=(self.rows - self.k, self.cols - self.k))
        right_proj = right_proj + self.n - self.n
        right_proj_outside[:, :, int(self.rows / 2) - int(right_proj.shape[2] / 2): int(self.rows / 2) + int(
            right_proj.shape[2] / 2), int(self.rows / 2) - int(right_proj.shape[2] / 2): int(self.rows / 2) + int(
            right_proj.shape[2] / 2)] = right_proj

        return front_proj_outside, back_proj_outside, left_proj_outside, right_proj_outside


# if __name__ == "__main__":
#     loss = nn.MSELoss()
#     root = 'data'
#     model = Model(os.path.join(root, 'final_project_point_cloud.fuse'),
#                   os.path.join(root, 'image', 'camera.config'))
#     optimizer = torch.optim.Adam(list(model.camera_config.values()), lr=1)
#     front, back, left, right = model()
#
#     cost = loss(back, back)
#     cost.backward()
#     optimizer.step()
#     print('done')
#     print(model.camera_config)
