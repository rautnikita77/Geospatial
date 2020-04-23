# Histogram eq -> Blur filter -> Mean

import cv2
from matplotlib import pyplot as plt
import numpy as np
from utils import apply_laplacian, hist_eq, subplot_img, plot_cam2_bounding_box, apply_thresholding_img, gaussian_blur
import os
from tqdm import tqdm

camera = 3
data_path = '/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/data/sample_drive/cam_' + str(camera)


if __name__ == '__main__':
    sum_ = 0
    for n, img in tqdm(enumerate(os.listdir(data_path))):
        image = cv2.imread(os.path.join(data_path, img))
        img_hist = hist_eq(image)
        # print(np.max(img_hist))
        # plot_cam2_bounding_box(img_hist, 4, 'hist')
        img_gauss = gaussian_blur(img_hist, 10)
        # plot_cam2_bounding_box(img_gauss, 4, 'guass')
        # break
        if isinstance(sum_, int):
            sum_ = img_gauss
        else:
            sum_ += img_gauss

    sum_ = sum_ / n
    print(np.max(sum_), np.min(sum_))
    plot_cam2_bounding_box(sum_, camera, 'final')
