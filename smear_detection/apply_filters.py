import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread(r'WhatsApp Image 2020-04-20 at 7.58.55 PM.jpeg')

# kernel = np.ones((5, 5), np.float32)/25
kernel = np.array([[0, -1, 0],
                  [-1, 4, -1],
                  [0, -1, 0]])
# dst = cv2.filter2D(img, -1, kernel)
median = cv2.medianBlur(img, 5)
new = img - median

plt.subplot(121), plt.imshow(new), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(median), plt.title('Averaging')
plt.xticks([]), plt.yticks([])
plt.show()