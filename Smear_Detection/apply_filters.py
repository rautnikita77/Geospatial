import cv2
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
import utils

# from apply_filters import apply_laplacian


def apply_laplacian(src):
    ddepth = cv2.CV_16S
    # src = cv2.imread(cv2.samples.findFile(r'WhatsApp Image 2020-04-20 at 7.58.55 PM.jpeg'), cv2.IMREAD_COLOR) # Load an image
    # src = cv2.resize(src, (500, 500))
    src = cv2.GaussianBlur(src, (3, 3), 0)
    # print(src)
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # print(src_gray)
    dst = cv2.Laplacian(src_gray, ddepth, ksize=3)
    print(dst)
    abs_dst = cv2.convertScaleAbs(dst)
    # print(abs_dst)
    return abs_dst


img = cv2.imread(r'393408669.jpg')
print(img.shape)

# img = 255 - img

# kernel = np.ones((5, 5), np.float32)/25
kernel = np.array([[0, -1, 0],
                  [-1, 4, -1],
                  [0, -1, 0]])
dst = cv2.filter2D(img, -1, kernel)
median = cv2.medianBlur(img, 25)
new = img - median

img2 = cdf[img]

# print(lap, np.max(lap))
# lap = (lap / np.max(lap)) * 255
# print(lap, np.max(lap))

plt.subplot(241), plt.imshow(img), plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(242), plt.imshow(new), plt.title('Og - median')
plt.xticks([]), plt.yticks([])
plt.subplot(243), plt.imshow(median), plt.title('Median')
plt.xticks([]), plt.yticks([])
plt.subplot(244), plt.imshow(dst), plt.title('Laplacian_2')
plt.xticks([]), plt.yticks([])
plt.subplot(245), plt.imshow(lap), plt.title('Laplacian')
plt.xticks([]), plt.yticks([])
plt.subplot(246), plt.imshow(img - img2 - cv2.cvtColor(lap, cv2.COLOR_GRAY2RGB)), plt.title('Og - hist')
plt.xticks([]), plt.yticks([])
plt.subplot(247), plt.imshow(img - img2), plt.title('Og - hist')
plt.xticks([]), plt.yticks([])


og_hist = img - img2
hist_threshold = np.where(og_hist > 200, 0, 255)
print(hist_threshold.shape, np.unique(hist_threshold))
plt.subplot(248), plt.imshow(hist_threshold), plt.title('Thresholding')
plt.xticks([]), plt.yticks([])
# cv2.imshow('a', hist_threshold)
# cv2.waitKey(0)

plt.show()

