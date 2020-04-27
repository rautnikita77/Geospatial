import cv2
import os
from utils import plot_bounding_box, erode, apply_thresholding_img, dilate, median_blur, gaussian_blur, custom_median_filter
import numpy as np


path = './means'


for means in os.listdir(path):
    camera = means[5:6]
    if camera != '2':
        continue
    mean = cv2.imread(os.path.join(path, means), 0)
    image = 255 - cv2.adaptiveThreshold(mean, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 75, 3)
    plot_bounding_box(image, title_='og camera ' + camera)
    lines = custom_median_filter(image, 301, 1)
    lines = dilate(lines, 3)
    plot_bounding_box(lines, title_='lines camera ' + camera)
    plot_bounding_box(image - lines, title_='img - lines camera ' + camera)

    image = image - lines
    cv2.imwrite('mask_' + camera + '.jpg', image)
    image = cv2.imread('mask_' + camera + '.jpg', 0)
    image = median_blur(image, 75, 1)
    image = dilate(image, 7, 7)
    image = 255 - apply_thresholding_img(image, 2, 255)
    image = dilate(image, 5, 15)
    image = median_blur(image, 51, 5)

    plot_bounding_box(image, title_='mask camera ' + camera)
