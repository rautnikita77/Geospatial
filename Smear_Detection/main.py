import cv2
from matplotlib import pyplot as plt
import numpy as np
from utils import apply_laplacian, hist_eq


def create_smear_mask(img):
    img_hist_eq = hist_eq(img)
    og_hist = img - img_hist_eq
    og_hist_gray = cv2.cvtColor(og_hist, cv2.COLOR_BGR2GRAY)
    hist_threshold = np.where(og_hist_gray > 200, 0, 255)
    return hist_threshold


if __name__ == "__main__":
    image = cv2.imread(r'393408669.jpg')
    mask = create_smear_mask(image)
    plt.imshow(mask)
    plt.show()