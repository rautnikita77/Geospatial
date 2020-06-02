import cv2
import matplotlib.pyplot as plt
import os
import numpy as np
from Point_Cloud_And_Image_Misalignment.utils import dilate, erode, median_blur, zoom_out


path = 'data'
img = cv2.imread(os.path.join(path, 'image/front.jpg'), 0)
img = img.astype(np.uint8)
# print(np.max(img))
img = dilate(img, 3, 5)
# img = erode(img, 3, 5)
edges1 = cv2.Canny(img, 100, 200)
edges1 = median_blur(edges1, 3, 1)

# cv2.imshow('a', edges)
# cv2.waitKey(0)
# plt.imshow(edges1)
# plt.show()
#
# cv2.imwrite('temp0.jpg', edges1)
#
# plt.imshow(img)
# plt.show()

projection = np.load(os.path.join(path, 'front.np.npy'))
projection = projection.astype(np.uint8)
# print(np.max(img))
projection = dilate(projection, 3, 5)
# projection = erode(projection, 3, 5)
edges = cv2.Canny(projection, 50, 200)
# edges = median_blur(edges, 3)
# edges = np.array([edges, np.zeros_like(edges), np.zeros_like(edges)]).transpose((1, 2, 0))
# edges1 = np.array([np.zeros_like(edges1), edges1, np.zeros_like(edges1)]).transpose((1, 2, 0))
# print(edges.shape, edges1.shape)
# plt.imshow(edges + edges1)
# plt.show()
#
# plt.imshow(projection + img, cmap='gray')
# plt.show()

# cv2.imwrite('temp1.jpg', edges + edges1)
plt.imshow(edges, cmap='gray')
plt.show()

rows, cols = img.shape
M = np.float32([[1, 0, 10], [0, 1, -10]])
edges = cv2.warpAffine(edges, M, (cols, rows))

edges = zoom_out(edges, (edges.shape[0]-50, edges.shape[1]-50))

plt.imshow(edges, cmap='gray')
plt.show()

loss = np.sum((edges[25:-25, 25:-25] - edges1[25:-25, 25:-25]) ** 2)
print(loss)

edges = np.array([edges, np.zeros_like(edges), np.zeros_like(edges)]).transpose((1, 2, 0))
edges1 = np.array([np.zeros_like(edges1), edges1, np.zeros_like(edges1)]).transpose((1, 2, 0))
print(edges.shape, edges1.shape)
plt.imshow(edges + edges1)
plt.show()

cv2.imwrite('temp0.jpg', edges + edges1)