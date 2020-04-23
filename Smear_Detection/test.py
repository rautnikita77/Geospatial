import cv2
import matplotlib.pyplot as plt
from utils import apply_thresholding_img, plot_cam2_bounding_box

img = cv2.imread('/Users/anupamtripathi/PycharmProjects/Geospatial/myplot')
cv2.rectangle(img, (1180, 780), (1300, 900), (255, 255, 0), 10)
img = apply_thresholding_img(img * 255, 100, 255)
plot_cam2_bounding_box(img)
plt.imshow(img)
plt.show()

# img = cv2.imread('/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/data/sample_drive/cam_2/393412418.jpg')
# # cv2.rectangle(img, (20, 20), (100, 100), (0, 0, 0), 2)
# rect = patches.Rectangle((50,100),40,30,linewidth=1,edgecolor='r',facecolor='none')
# plt.imshow(img)
# plt.add_patch(rect)
# plt.show()