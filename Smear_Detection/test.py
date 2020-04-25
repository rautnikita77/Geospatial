import cv2
import matplotlib.pyplot as plt
from utils import apply_thresholding_img, plot_bounding_box, gaussian_blur, median_blur
import numpy as np

img = cv2.imread('/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/test3.jpg', cv2.IMREAD_GRAYSCALE)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = 255 - img
plot_bounding_box(img, 5)
print(img.dtype)
kernel = np.ones((3, 3), np.uint8)
bg = cv2.dilate(img, kernel, iterations=1)
plot_bounding_box(bg, 5)
plot_bounding_box(img - bg, 5)
# plot_cam2_bounding_box(bg, 3, 'bg')
# plot_cam2_bounding_box(img - bg, 3, 'img-bg')
# fig, ax = plt.subplots(nrows=5, ncols=5)
# count = 3
# for row in ax:
#     for col in row:
#         col.imshow(cv2.medianBlur(img - bg, count))
#         count += 2
# plt.show()
temp = median_blur(img, 15, 5)
print(temp, np.max(temp))
# tem = cv2.medianBlur(temp, 101)
plot_bounding_box(cv2.medianBlur(temp, 15), 5)

# img = cv2.imread('/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/data/sample_drive/cam_2/393412418.jpg')
# # cv2.rectangle(img, (20, 20), (100, 100), (0, 0, 0), 2)
# rect = patches.Rectangle((50,100),40,30,linewidth=1,edgecolor='r',facecolor='none')
# plt.imshow(img)
# plt.add_patch(rect)
# plt.show()