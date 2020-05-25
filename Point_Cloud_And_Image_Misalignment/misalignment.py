import cv2
import matplotlib.pyplot as plt
import os
import numpy as np
from Point_Cloud_And_Image_Misalignment.utils import dilate, erode


path = 'data'
img = cv2.resize(cv2.imread(os.path.join(path, 'image/front.jpg'), 0), (512, 512))
img = img.astype(np.uint8)
# print(np.max(img))
# img = dilate(img, 3, 5)
# img = erode(img, 3, 5)
edges = cv2.Canny(img, 100, 200)

# cv2.imshow('a', edges)
# cv2.waitKey(0)
plt.imshow(edges)
plt.show()

cv2.imwrite('temp0.jpg', edges)

plt.imshow(img)
plt.show()

projection = np.load(os.path.join(path, 'front.np.npy'))
projection = projection.astype(np.uint8)
# print(np.max(img))
# projection = dilate(projection, 3, 5)
# projection = erode(projection, 3, 5)
edges = cv2.Canny(projection, 50, 200)

plt.imshow(edges)
plt.show()

plt.imshow(projection)
plt.show()

cv2.imwrite('temp1.jpg', edges)