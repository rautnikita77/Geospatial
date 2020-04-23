import cv2
import numpy as np
import matplotlib.pyplot as plt


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


def subplot_img(imgs, title='Subplots'):
    fig, axes = plt.subplots(len(imgs))
    for x in range(len(imgs)):
        axes[x].imshow(imgs[x])
    plt.show()


def gaussian_blur(img, size):
    kernel = np.ones((size, size), np.float32) / (size**2)
    dst = cv2.filter2D(img, -1, kernel)
    return dst


def plot_cam2_bounding_box(img, camera=2, title_=''):
    if camera == 2:
        cv2.rectangle(img, (1180, 780), (1300, 900), (122, 0, 0), 10)
    if camera == 3:
        cv2.rectangle(img, (1760, 1420), (1950, 1600), (122, 0, 0), 10)
    plt.imshow(img, cmap='gray')
    # plt.imshow(img[1180:1300, 780:900], cmap='gray')
    plt.title(title_)
    plt.show()
    # print(img[1180:1300, 780:900])


def apply_thresholding_img(img, t1, t2):
    hist_threshold = np.where(img >= t1, img, 255)
    hist_threshold = np.where(hist_threshold < t2, 0, hist_threshold)
    return hist_threshold
