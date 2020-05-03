import cv2
import numpy as np
from utils import plot_bounding_box, erode, dilate, median_blur, gaussian_blur
import os
from tqdm import tqdm

camera = 3
data_path = 'data/sample_drive/cam_' + str(camera)


def detect_smear_camer(camera):
    mean = cv2.imread(os.path.join(data_path, os.listdir(data_path)[0]), 0)
    equ = cv2.equalizeHist(mean)
    mean = cv2.GaussianBlur(equ, (9, 9), 0)
    for n, img in enumerate(tqdm(os.listdir(data_path)[1:])):
        image = cv2.imread(os.path.join(data_path, img), cv2.IMREAD_GRAYSCALE)
        equ = cv2.equalizeHist(image)
        equ = cv2.GaussianBlur(equ, (9, 9), 0)
        mean = (mean * (n + 1) + equ) / (n + 2)

    cv2.imwrite("mean.png", mean)
    mean = cv2.imread('mean.png')
    # plot_bounding_box(mean, -1, 'Mean camera ' + str(camera))
    kernel = np.ones((3, 3), np.uint8)
    bg = cv2.dilate(mean, kernel, iterations=1)
    mask = mean - bg
    cv2.imwrite("bg2.png", mask)
    # plot_bounding_box(mask, -1, 'Foreground ' + str(camera))
    for iterations in range(2):
        mask = cv2.medianBlur(mask, 101)

    cv2.imwrite("a.png", mask)
    plot_bounding_box(mask, -1, 'Mask camera ' + str(camera))

    params = cv2.SimpleBlobDetector_Params()

    params.filterByArea = True
    params.minArea = 300
    params.maxArea = mask.shape[0] * mask.shape[1] / 2

    mask = 255 - mask
    detector = cv2.SimpleBlobDetector_create(params)


if __name__ == "__main__":
    detect_smear_camer(3)
