import torch
import torch.nn as nn
from Point_Cloud_And_Image_Misalignment.model2 import Model
from Point_Cloud_And_Image_Misalignment.utils import dilate, zoom_out
from tqdm import tqdm
import os
import cv2
import numpy as np


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
root = 'data'

lr = 0.01
epochs = 300

def train():

    front_img = cv2.imread(os.path.join(root, 'image', 'front.jpg'), 0)
    _, front_img = cv2.threshold(front_img, 210, 255, cv2.THRESH_BINARY)
    front_proj = cv2.imread(os.path.join(root, 'projections', 'front.jpg'), 0)
    front_proj = dilate(front_proj, 3, 5)
    _, front_proj = cv2.threshold(front_proj, 50, 255, cv2.THRESH_BINARY)
    zeros = np.zeros_like(front_img)

    initial = np.stack((front_img, front_proj, zeros), axis=2)
    cv2.imwrite(os.path.join(root, 'outputs', 'initial.png'), initial)

    back_img = cv2.imread(os.path.join(root, 'image', 'back.jpg'), 0)
    left_img = cv2.imread(os.path.join(root, 'image', 'left.jpg'), 0)
    right_img = cv2.imread(os.path.join(root, 'image', 'right.jpg'), 0)


    _, back_img = cv2.threshold(back_img, 210, 255, cv2.THRESH_BINARY)
    _, left_img = cv2.threshold(left_img, 210, 255, cv2.THRESH_BINARY)
    _, right_img = cv2.threshold(right_img, 210, 255, cv2.THRESH_BINARY)

    front_img = torch.from_numpy(front_img).float()
    back_img = torch.from_numpy(back_img).float()
    left_img = torch.from_numpy(left_img).float()
    right_img = torch.from_numpy(right_img).float()



    back_proj = cv2.imread(os.path.join(root, 'projections', 'back.jpg'), 0)
    left_proj = cv2.imread(os.path.join(root, 'projections', 'left.jpg'), 0)
    right_proj = cv2.imread(os.path.join(root, 'projections', 'right.jpg'), 0)


    back_proj = dilate(back_proj, 3, 5)
    left_proj = dilate(left_proj, 3, 5)
    right_proj = dilate(right_proj, 3, 5)


    _, back_proj = cv2.threshold(back_proj, 50, 255, cv2.THRESH_BINARY)
    _, left_proj = cv2.threshold(left_proj, 50, 255, cv2.THRESH_BINARY)
    _, right_proj = cv2.threshold(right_proj, 50, 255, cv2.THRESH_BINARY)

    front_proj = torch.from_numpy(front_proj).float()
    back_proj = torch.from_numpy(back_proj).float()
    left_proj = torch.from_numpy(left_proj).float()
    right_proj = torch.from_numpy(right_proj).float()

    front_proj = front_proj.unsqueeze(0).unsqueeze(0)
    back_proj = back_proj.unsqueeze(0).unsqueeze(0)
    left_proj = left_proj.unsqueeze(0).unsqueeze(0)
    right_proj = right_proj.unsqueeze(0).unsqueeze(0)

    rows, cols = front_img.shape

    front_img = front_img.unsqueeze(0).unsqueeze(0)
    back_img = back_img.unsqueeze(0).unsqueeze(0)
    left_img = left_img.unsqueeze(0).unsqueeze(0)
    right_img = right_img.unsqueeze(0).unsqueeze(0)

    imgs = torch.stack((front_img, back_img, left_img, right_img))


    loss = nn.MSELoss()
    model = Model(rows, cols)

    # print(model.M_tune)
    optimizer = torch.optim.Adam([model.M_tune, model.n], lr=lr)

    for epoch in range(epochs):

        optimizer.zero_grad()

        front_proj_, back_proj_, left_proj_, right_proj_ = model(front_proj, back_proj, left_proj, right_proj)
        projs = torch.stack((front_proj_, back_proj_, left_proj_, right_proj_))

        imgs = imgs.to(device)
        projs = projs.to(device)

        cost = loss(imgs, projs)
        cost.backward(retain_graph=True)
        optimizer.step()

        print(model.M_tune)
        print(model.n)





        print('Epoch: {}    Train Loss =  {}'.format(epoch, cost))


    front_proj_np = front_proj.squeeze(0).squeeze(0).clone().detach().numpy()
    front_proj_np = cv2.warpAffine(front_proj_np, model.M_tune.detach().numpy()[0], (rows, cols))
    front_proj_np = zoom_out(front_proj_np, (
        int(front_proj_np.shape[0] - model.n.detach().numpy()[0]),
        int(front_proj_np.shape[1] - model.n.detach().numpy()[0])))
    front_img_np = front_img.squeeze(0).squeeze(0).clone().detach().numpy()
    zeros = np.zeros_like(front_img_np)
    a = np.stack((front_img_np, front_proj_np, zeros), axis=2)
    numpy_horizontal = np.hstack((front_img_np, front_proj_np))
    cv2.imwrite(os.path.join(root, 'outputs', 'result.png'), numpy_horizontal)
    cv2.imwrite(os.path.join(root, 'outputs', 'result1.png'), a)



if __name__ == "__main__":
    train()
