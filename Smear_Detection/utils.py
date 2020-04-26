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


def apply_laplacian(src, size):
    ddepth = cv2.CV_16S
    src = cv2.GaussianBlur(src, (size, size), 0)
    # src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    dst = cv2.Laplacian(src, ddepth, ksize=size)
    abs_dst = cv2.convertScaleAbs(dst)
    return abs_dst


def edge_detection(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged


def subplot_img(imgs, title='Subplots'):
    fig, axes = plt.subplots(len(imgs))
    for x in range(len(imgs)):
        axes[x].imshow(imgs[x])
    plt.show()


def gaussian_blur(img, size, iterations=1):
    for x in range(iterations):
        img = cv2.GaussianBlur(img, (size, size), 0)
    return img


def plot_bounding_box(img, camera=-1, title_=''):
    if camera == 0:
        cv2.rectangle(img, (850, 620), (1050, 800), (122, 0, 0), 10)
    elif camera == 2:
        cv2.rectangle(img, (1180, 780), (1300, 900), (122, 0, 0), 10)
    elif camera == 3:
        cv2.rectangle(img, (1760, 1420), (1950, 1600), (122, 0, 0), 10)
    elif camera == 5:
        cv2.rectangle(img, (1610, 1580), (1780, 1770), (122, 0, 0), 10)
    plt.imshow(img, cmap='gray')
    plt.title(title_)
    plt.show()


def apply_thresholding_img(img, t1, t2):
    hist_threshold = np.where(img >= t1, img, 255)
    hist_threshold = np.where(hist_threshold < t2, 0, hist_threshold)
    return hist_threshold


def dilate(img, size, iterations=1):
    kernel = np.ones((size, size), np.uint8)
    bg = cv2.dilate(img, kernel, iterations=iterations)
    return bg


def erode(img, size, iterations=1):
    kernel = np.ones((size, size), np.uint8)
    bg = cv2.erode(img, kernel, iterations=iterations)
    return bg


def median_blur(img, size, iterations=1):
    for iterations in range(iterations):
        img = cv2.medianBlur(img, size)
    return img


def isolate_key_ponits(mask, keypoints):
    new_mask = np.zeros(mask.shape) * 255
    for y, x in keypoints[0].convert(keypoints):
        x = int(x)
        y = int(y)
        print(x, y)
        new_mask[x - 100: x + 100, y - 100: y + 100] = mask[x - 100: x + 100, y - 100: y + 100]
    return new_mask
