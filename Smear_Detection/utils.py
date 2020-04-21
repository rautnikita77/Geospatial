import cv2
import numpy as np


def hist_eq(img):
    hist, bins = np.histogram(img.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_m = np.ma.masked_equal(cdf, 0)
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')
    img2 = cdf[img]
    return img2


def apply_laplacian(src):
    ddepth = cv2.CV_16S
    src = cv2.GaussianBlur(src, (3, 3), 0)
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    dst = cv2.Laplacian(src_gray, ddepth, ksize=3)
    abs_dst = cv2.convertScaleAbs(dst)
    return abs_dst