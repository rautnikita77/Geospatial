import cv2
import matplotlib.pyplot as plt
from utils import apply_thresholding_img, plot_bounding_box, gaussian_blur, median_blur, dilate, erode
import numpy as np

# img = cv2.imread('/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/mean.png')
# plt.imshow(img - dilate(img, 3, 1), cmap='gray')
# plt.show()
# plt.imshow(img - dilate(img, 7, 1), cmap='gray')
# plt.show()
# plt.imshow(img - dilate(img, 3, 3), cmap='gray')
# plt.show()
# plt.imshow(img - dilate(img, 3, 7), cmap='gray')
# plt.show()
# img_equ = cv2.equalizeHist(img)
# plt.imshow(img_equ)
# plt.show()
# plt.imshow(gaussian_blur(img_equ, 7), cmap='gray')
# plt.show()
# plt.imshow(img - img_equ, cmap='gray')
# plt.show()
# plt.imshow(gaussian_blur(img_equ, 15), cmap='gray')
# plt.show()
# plt.imshow(gaussian_blur(img - img_equ, 15), cmap='gray')
# plt.show()
# plt.imshow(img - img_equ, cmap='gray')
# plt.show()
# cv2.imwrite('ppt2.jpg', img)
# cv2.imwrite('ppt1.jpg', img_equ)
# cv2.waitKey(0)
# # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img = 255 - img
# plot_bounding_box(img, 5)
# print(img.dtype)
# kernel = np.ones((3, 3), np.uint8)
# bg = cv2.dilate(img, kernel, iterations=1)
# plot_bounding_box(bg, 5)
# plot_bounding_box(img - bg, 5)
# # plot_cam2_bounding_box(bg, 3, 'bg')
# # plot_cam2_bounding_box(img - bg, 3, 'img-bg')
# # fig, ax = plt.subplots(nrows=5, ncols=5)
# # count = 3
# # for row in ax:
# #     for col in row:
# #         col.imshow(cv2.medianBlur(img - bg, count))
# #         count += 2
# # plt.show()
# temp = median_blur(img, 15, 5)
# print(temp, np.max(temp))
# # tem = cv2.medianBlur(temp, 101)
# plot_bounding_box(cv2.medianBlur(temp, 15), 5)

# img = cv2.imread('/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/data/sample_drive/cam_2/393412418.jpg')
# # cv2.rectangle(img, (20, 20), (100, 100), (0, 0, 0), 2)
# rect = patches.Rectangle((50,100),40,30,linewidth=1,edgecolor='r',facecolor='none')
# plt.imshow(img)
# plt.add_patch(rect)
# plt.show()
import os


dir = '/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/means'
for img in os.listdir(dir):
    camera = int(img[4:5])
    image = cv2.imread(os.path.join(dir, img))
    bg = dilate(image, 3, iterations=1)
    mask = image - bg
    # plot_bounding_box(mask, camera, 'Mask camera ' + str(camera))
    # mask = median_blur(mask, 51, 4)
    mask = erode(mask, 3, 2)
    mask = median_blur(mask, 7, 4)
    mask = dilate(mask, 11, 5)
    # mask = dilate(mask, 3, iterations=1)
    plot_bounding_box(mask, camera, 'Mask camera ' + str(camera))
    # cv2.imshow('a', mask)
    # cv2.waitKey(0)

# img = cv2.imread('test3.jpg')
# plt.imshow(255 - img)
# plt.show()
# mean = 255 - img
# bg = dilate(mean, 3, iterations=1)
# plot_bounding_box(mean - bg, 5, 'BG ' + str(5))
# mask = mean - bg
# print(mask.dtype, np.max(mask))
# mask = median_blur(mask, 101, 2)
# plot_bounding_box(mask, 5, 'Mask camera ' + str(5))
