import cv2
from matplotlib import pyplot as plt
import numpy as np
from utils import hist_eq, plot_bounding_box, erode, dilate, median_blur
import os
from tqdm import tqdm

camera = 5
data_path = 'data/sample_drive/cam_' + str(camera)


def detect_smear_camer(camera):
    mean = cv2.imread(os.path.join(data_path, os.listdir(data_path)[0]), cv2.IMREAD_GRAYSCALE)
    for n, img in enumerate(tqdm(os.listdir(data_path)[1:])):
        image = cv2.imread(os.path.join(data_path, img), cv2.IMREAD_GRAYSCALE)
        equ = cv2.equalizeHist(image)
        mean = (mean * (n + 1) + equ) / (n + 2)

    mean = cv2.cvtColor(mean.astype(np.uint8), cv2.COLOR_GRAY2RGB)
    plot_bounding_box(mean, -1, 'Mean camera ' + str(camera))
    bg = dilate(mean, 3, iterations=1)
    mask = mean - bg
    plot_bounding_box(mask, -1, 'Foreground ' + str(camera))
    mask = erode(mask, 3, 2)
    mask = median_blur(mask, 7, 4)
    mask = dilate(mask, 11, 5)
    plot_bounding_box(mask, -1, 'Mask camera ' + str(camera))


if __name__ == "__main__":
    detect_smear_camer(camera)
