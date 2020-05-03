import cv2
import matplotlib.pyplot as plt
import numpy as np
from utils import custom_median_filter, median_blur, erode, plot_bounding_box, dilate, rotate_with_pading, custom_median_filter_range, apply_thresholding_img

# image = cv2.imread('/Users/anupamtripathi/PycharmProjects/Geospatial/test.jpg', 0)
# image = 255 - cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 75, 3)
# image = cv2.resize(image, (1000, 1000))
# plot_bounding_box(image)
#
# lines = custom_median_filter_range(image, 75, 1, 15)
# lines = dilate(lines, 3)
# plot_bounding_box(lines)
# plot_bounding_box(image - lines)

# image = rotate_with_pading(image, 45)
# lines = custom_median_filter(image, 101, 11)
# lines = dilate(lines, 3)
# plot_bounding_box(lines)
# # plot_bounding_box(image - lines)
# #
# for camera in ['2', '3', '5']:
#     image = cv2.imread('mask_' + camera + '.jpg', 0)
#     image = median_blur(image, 75, 1)
#     # plot_bounding_box(image)
#     # image = erode(image, 7, 3)
#     image = dilate(image, 7, 7)
#     image = 255 - apply_thresholding_img(image, 2, 255)
#     image = dilate(image, 5, 15)
#     image = median_blur(image, 51, 5)
#     plot_bounding_box(image)

image = cv2.imread('/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/data/sample_drive/cam_2/393408762.jpg', 0)
plot_bounding_box(cv2.equalizeHist(image))
