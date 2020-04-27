import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


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


def custom_median_filter(img_og, size, line_size):
    img = np.copy(img_og)
    padding = int((size-1)/2)
    img_og = cv2.copyMakeBorder(img_og, padding, padding, padding, padding, cv2.BORDER_CONSTANT)

    r_left = int((line_size-1)/2)
    r_right = int((line_size-1)/2)+1
    c_up = int((size-1)/2)
    c_down = int((size-1)/2)+1
    for r, row in enumerate(tqdm(img)):
        for c, pixel in enumerate(row):
            r_og = r + padding
            c_og = c + padding
            filtered_area = img_og[r_og-r_left: r_og+r_right, c_og-c_up: c_og+c_down]
            img[r, c] = np.median(filtered_area)
    return img


def custom_median_filter_range(img_og, size, line_size_1, line_size_2):
    img_1 = np.copy(img_og)
    img_2 = np.copy(img_og)
    # ones = np.ones((line_size, size))
    # remaining_filter_size = size - line_size
    # zeros = np.zeros((int(remaining_filter_size/2), size))
    # median_filter = np.concatenate((zeros, ones, np.copy(zeros)), axis=0)
    # print(median_filter, median_filter.shape)
    r_left_1 = int((line_size_1 - 1) / 2)
    r_right_1 = int((line_size_1 - 1) / 2) + 1
    r_left_2 = int((line_size_2 - 1) / 2)
    r_right_2 = int((line_size_2 - 1) / 2) + 1
    c_up = int((size - 1) / 2)
    c_down = int((size - 1) / 2) + 1
    for r, row in enumerate(tqdm(img_og)):
        for c, pixel in enumerate(row):
            # print('\n\npixel ', pixel)
            # print('row ', max(0, r-int((line_size-1)/2)), min(img.shape[0], r+int((line_size-1)/2)+1))
            # print('col ', max(0, c-int((size-1)/2)), min(img.shape[0], c+int((size-1)/2)+1))
            filtered_area_1 = img_og[max(0, r-r_left_1): min(img_og.shape[0], r+r_right_1),
                            max(0, c-c_up): min(img_og.shape[0], c+c_down)]
            filtered_area_2 = img_og[max(0, r - r_left_2): min(img_og.shape[0], r + r_right_2),
                            max(0, c - c_up): min(img_og.shape[0], c + c_down)]
            img_1[r, c] = np.median(filtered_area_1)
            img_2[r, c] = np.median(filtered_area_2)
            # print(filtered_area.shape)
            # print(filtered_area)
            # if c == 3:
            #     break
        # if r == 2:
        #     break
    plot_bounding_box(img_1)
    plot_bounding_box(img_2)
    return img_1 + img_2


def rotate_with_pading(img, angle):
    if angle != 0 or angle != 90 or angle != -90:
        padding = int(((2**0.5)*img.shape[0] - img.shape[0])/2)
        # print(padding)
        img = cv2.copyMakeBorder(img, padding, padding, padding, padding, cv2.BORDER_CONSTANT)
    rows, cols = img.shape

    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    dst = cv2.warpAffine(img, M, (cols, rows))
    # plot_bounding_box(dst)
    return dst


def undo_rotate(img, angle):
    if angle != 0 or angle != 90 or angle != -90:
        padding = int(((2 ** 0.5) * img.shape[0] - img.shape[0]) / 2)


if __name__ == '__main__':
    rotate_with_pading((np.arange(10000)).astype(np.uint8).reshape((100, 100)), 0)
