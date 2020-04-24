# Histogram eq -> Blur filter -> Mean

import cv2
from matplotlib import pyplot as plt
import numpy as np
from utils import apply_laplacian, hist_eq, subplot_img, plot_cam2_bounding_box, apply_thresholding_img, gaussian_blur, edge_detection
import os
from tqdm import tqdm

camera = 2
data_path = '/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/data/sample_drive/cam_' + str(camera)


if __name__ == '__main__':
    mean = []
    for n, img in tqdm(enumerate(os.listdir(data_path))):
        image = cv2.imread(os.path.join(data_path, img), cv2.IMREAD_GRAYSCALE)
        img_hist = hist_eq(image)
        # print(np.max(img_hist))
        # plot_cam2_bounding_box(img_hist, 4, 'hist')
        img_gauss = gaussian_blur(img_hist, 10)
        # plot_cam2_bounding_box(img_gauss, 4, 'guass')
        # break
        # if isinstance(sum_, int):
        #     sum_ = img_gauss
        # else:
        #     sum_ = sum_ + img_gauss
        #     print(np.max(sum_), np.min(sum_), np.max(img_gauss))
        mean.append(img_gauss)
        # if n == 100:
        #     break

    mean = np.array(mean)
    mean = np.mean(mean, axis=0)
    plot_cam2_bounding_box(mean, camera, 'final')
    # plot_cam2_bounding_box(apply_laplacian(mean, 3), camera)
    cv2.imwrite('test2.jpg', mean)

