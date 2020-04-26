import cv2
import numpy as np
from utils import plot_bounding_box, erode, dilate, median_blur, gaussian_blur
import os
from tqdm import tqdm

camera = 2
data_path = 'data/sample_drive/cam_' + str(camera)


def detect_smear_camer(camera):
    mean = cv2.imread(os.path.join(data_path, os.listdir(data_path)[0]), cv2.IMREAD_GRAYSCALE)
    equ = cv2.equalizeHist(mean)
    mean = gaussian_blur(mean - equ, 9)
    for n, img in enumerate(tqdm(os.listdir(data_path)[1:])):
        image = cv2.imread(os.path.join(data_path, img), cv2.IMREAD_GRAYSCALE)
        equ = cv2.equalizeHist(image)
        equ = image - equ
        equ = gaussian_blur(equ, 9)
        mean = (mean * (n + 1) + equ) / (n + 2)

    mean = cv2.cvtColor(mean.astype(np.uint8), cv2.COLOR_GRAY2RGB)
    # plot_bounding_box(mean, -1, 'Mean camera ' + str(camera))
    bg = dilate(mean, 3, iterations=1)
    mask = mean - bg
    # plot_bounding_box(mask, -1, 'Foreground ' + str(camera))
    mask = median_blur(mask, 101, 2)
    plot_bounding_box(mask, -1, 'Mask camera ' + str(camera))

    params = cv2.SimpleBlobDetector_Params()

    params.filterByArea = True
    params.minArea = 300
    params.maxArea = mask.shape[0] * mask.shape[1] / 2

    mask = 255 - mask
    detector = cv2.SimpleBlobDetector_create(params)


if __name__ == "__main__":
    detect_smear_camer(3)
