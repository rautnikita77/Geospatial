import cv2
from matplotlib import pyplot as plt
import numpy as np
from utils import hist_eq, plot_bounding_box, gaussian_blur, dilate, median_blur
import os
from tqdm import tqdm

camera = 5
data_path = '/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/data/new_data/sample_drive/cam_' + str(camera)


if __name__ == "__main__":
    mean = cv2.imread(os.path.join(data_path, os.listdir(data_path)[0]), cv2.IMREAD_GRAYSCALE)
    # mean2 = cv2.imread(os.path.join(data_path, os.listdir(data_path)[0]), cv2.IMREAD_GRAYSCALE)
    for n, img in tqdm(enumerate(os.listdir(data_path)[1:])):
        image = cv2.imread(os.path.join(data_path, img), cv2.IMREAD_GRAYSCALE)
        image = 255 - image
        equ = cv2.equalizeHist(image)
        # equ = image - equ
        mean = (mean * (n + 1) + equ) / (n + 2)
        # mean2 = (mean2 * (n + 1) + image - equ) / (n + 2)
        # if n == 500:
        #     break

    # mean = np.array(mean)
    # mean = np.mean(mean, axis=0)
    print(mean.dtype, mean.shape, np.max(mean))
    cv2.imwrite('test3.jpg', mean)
    mean = cv2.imread('test3.jpg')
    # cv2.imwrite('test3.jpg', mean2)
    # mean2 = cv2.imread('test3.jpg', cv2.IMREAD_GRAYSCALE)
    print(mean.dtype, mean.shape, np.max(mean))
    plot_bounding_box(mean, camera, 'Mean camera ' + str(camera))
    # plot_bounding_box(mean2, camera, 'Mean camera ' + str(camera))
    bg = dilate(mean, 3, iterations=1)
    plot_bounding_box(mean - bg, camera, 'BG ' + str(camera))
    mask = mean - bg
    print(mask.dtype, np.max(mask))
    mask = median_blur(mask, 101, 2)
    plot_bounding_box(mask, camera, 'Mask camera ' + str(camera))
