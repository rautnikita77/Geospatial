import torch
from torch.utils.data import DataLoader
import torch.nn as nn
from Point_Cloud_And_Image_Misalignment.model import Model
from tqdm import tqdm
import os
import cv2
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
root = 'data'

lr = 0.001
epochs = 1

def train():
    point_cloud = os.path.join(root, 'final_project_point_cloud.fuse')
    camera_config = os.path.join(root, 'image', 'camera.config')


    front_img = cv2.imread(os.path.join(root, 'image', 'front.jpg'), 0)
    back_img = cv2.imread(os.path.join(root, 'image', 'back.jpg'), 0)
    left_img = cv2.imread(os.path.join(root, 'image', 'left.jpg'), 0)
    right_img = cv2.imread(os.path.join(root, 'image', 'right.jpg'), 0)

    _, front_img = cv2.threshold(front_img, 210, 255, cv2.THRESH_BINARY)
    _, back_img = cv2.threshold(back_img, 210, 255, cv2.THRESH_BINARY)
    _, left_img = cv2.threshold(left_img, 210, 255, cv2.THRESH_BINARY)
    _, right_img = cv2.threshold(right_img, 210, 255, cv2.THRESH_BINARY)

    front_img = torch.from_numpy(front_img).float()
    back_img = torch.from_numpy(back_img).float()
    left_img = torch.from_numpy(left_img).float()
    right_img = torch.from_numpy(right_img).float()

    imgs = torch.stack((front_img, back_img, left_img, right_img))

    rows, cols = front_img.shape

    loss = nn.MSELoss()
    model = Model(point_cloud, camera_config)
    model = model.to(device)

    optimizer = torch.optim.Adam(list(model.camera_config.values()), lr=lr)

    for epoch in range(epochs):

        optimizer.zero_grad()
        front_proj, back_proj, left_proj, right_proj = model()

        front_proj_np = front_proj.clone().detach().cpu().numpy()
        back_proj_np = back_proj.clone().detach().cpu().numpy()
        left_proj_np = left_proj.clone().detach().cpu().numpy()
        right_proj_np = right_proj.clone().detach().cpu().numpy()

        _, front_proj_np = cv2.threshold(front_proj_np, 50, 255, cv2.THRESH_BINARY)
        _, back_proj_np = cv2.threshold(back_proj_np, 50, 255, cv2.THRESH_BINARY)
        _, left_proj_np = cv2.threshold(left_proj_np, 50, 255, cv2.THRESH_BINARY)
        _, right_proj_np = cv2.threshold(right_proj_np, 50, 255, cv2.THRESH_BINARY)

        front_proj.data = torch.from_numpy(front_proj_np)
        back_proj.data = torch.from_numpy(back_proj_np)
        left_proj.data = torch.from_numpy(left_proj_np)
        right_proj.data = torch.from_numpy(right_proj_np)


        projs = torch.stack((front_proj, back_proj, left_proj, right_proj))

        imgs = imgs.to(device)
        projs = projs.to(device)

        cost = loss(imgs, projs)
        cost.backward()
        optimizer.step()

        print('Epoch: {}    Train Loss =  {}'.format(epoch, cost))
        print(model.camera_config)



if __name__ == "__main__":
    train()
