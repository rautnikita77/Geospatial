import cv2
import numpy as np
from matplotlib import pyplot as plt

from apply_filters import apply_laplacian

img = cv2.imread(r'393408689.jpg')

img = 255 - img

# kernel = np.ones((5, 5), np.float32)/25
kernel = np.array([[0, -1, 0],
                  [-1, 4, -1],
                  [0, -1, 0]])
dst = cv2.filter2D(img, -1, kernel)
median = cv2.medianBlur(img, 25)
new = img - median

lap = apply_laplacian.apply_laplacian(img)

plt.subplot(241), plt.imshow(img), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(242), plt.imshow(new), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(243), plt.imshow(median), plt.title('Averaging')
plt.xticks([]), plt.yticks([])
plt.subplot(244), plt.imshow(dst), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(245), plt.imshow(lap), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.show()