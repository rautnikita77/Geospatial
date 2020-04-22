import cv2
import matplotlib.pyplot as plt

img = cv2.imread('/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/data/sample_drive/cam_2/393412417.jpg')
cv2.rectangle(img, (1180, 780), (1300, 900), (255, 0, 0), 10)
plt.imshow(img)
plt.show()

# img = cv2.imread('/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/data/sample_drive/cam_2/393412418.jpg')
# # cv2.rectangle(img, (20, 20), (100, 100), (0, 0, 0), 2)
# rect = patches.Rectangle((50,100),40,30,linewidth=1,edgecolor='r',facecolor='none')
# plt.imshow(img)
# plt.add_patch(rect)
# plt.show()