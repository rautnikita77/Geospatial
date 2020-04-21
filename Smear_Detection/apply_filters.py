import cv2
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
from utils import apply_laplacian, hist_eq

# from apply_filters import apply_laplacian



img = cv2.imread(r'393408669.jpg')
print(img.shape)


img_hist_eq = hist_eq(img)

#
# plt.subplot(241), plt.imshow(img), plt.title('Original')
# plt.xticks([]), plt.yticks([])
# plt.subplot(242), plt.imshow(new), plt.title('Og - median')
# plt.xticks([]), plt.yticks([])
# plt.subplot(243), plt.imshow(median), plt.title('Median')
# plt.xticks([]), plt.yticks([])
# plt.subplot(244), plt.imshow(dst), plt.title('Laplacian_2')
# plt.xticks([]), plt.yticks([])
# plt.subplot(245), plt.imshow(lap), plt.title('Laplacian')
# plt.xticks([]), plt.yticks([])
# plt.subplot(246), plt.imshow(img - img2 - cv2.cvtColor(lap, cv2.COLOR_GRAY2RGB)), plt.title('Og - hist')
# plt.xticks([]), plt.yticks([])
# plt.subplot(247), plt.imshow(img - img2), plt.title('Og - hist')
# plt.xticks([]), plt.yticks([])




if __name__ == '__main__':
    img = cv2.imread(r'393408669.jpg')
    img_hist_eq = hist_eq(img)
    og_hist = img - img_hist_eq
    og_hist_gray = cv2.cvtColor(og_hist, cv2.COLOR_BGR2GRAY)
    hist_threshold = np.where(og_hist_gray > 200, 0, 255)

