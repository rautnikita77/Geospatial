import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


def plot_bounding_box(img, camera=-1, title_=''):
    """
    Plot image with bounding box
    Args:
        img (ndarray): Input image
        camera (int): Camera number
        title_ (str): Title for plot
    """
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
    """
    Apply binary thresholding to image
    Args:
        img (ndarray): input image
        t1 (int): Threshold lower bound
        t2 (int): Threshold upper bound

    Returns:
        Image after thresholding
    """
    hist_threshold = np.where(img >= t1, img, 255)
    hist_threshold = np.where(hist_threshold < t2, 0, hist_threshold)
    return hist_threshold


def dilate(img, size, iterations=1):
    """
    Apply binary dilation to image for given number of iterations
    Args:
        img (ndarray): input image
        size (int): Filter size
        iterations (int): Number of iterations

    Returns:
        Image after dilation
    """
    kernel = np.ones((size, size), np.uint8)
    bg = cv2.dilate(img, kernel, iterations=iterations)
    return bg


def erode(img, size, iterations=1):
    """
    Apply erosion to image for given number of iterations
    Args:
        img (ndarray): input image
        size (int): Filter size
        iterations (int): Number of iterations

    Returns:
        Image after erosion
    """
    kernel = np.ones((size, size), np.uint8)
    bg = cv2.erode(img, kernel, iterations=iterations)
    return bg


def median_blur(img, size, iterations=1):
    """
    Apply median blur to image for given number of iterations
    Args:
        img (ndarray): input image
        size (int): Filter size
        iterations (int): Number of iterations

    Returns:
        Image after median blur
    """
    for iterations in range(iterations):
        img = cv2.medianBlur(img, size)
    return img\


def isolate_key_ponits(mask, keypoints):
    """
    Generate mask from key points detected
    Args:
        mask (ndarray): original mask
        keypoints (cv2.keypoints): keypoints object

    Returns:
        mask for key points
    """
    new_mask = np.zeros(mask.shape) * 255
    for y, x in keypoints[0].convert(keypoints):
        x = int(x)
        y = int(y)
        print(x, y)
        new_mask[x - 100: x + 100, y - 100: y + 100] = mask[x - 100: x + 100, y - 100: y + 100]
    return new_mask


def custom_median_filter(img_og, size, line_size):
    """
    Apply a custom median blur
    Args:
        img (ndarray): input image
        size (int): Filter size
        line_size (int): Width of filter

    Returns:
        Image after median blur
    """
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
    """
    Apply a custom median blur for given range of line size
    Args:
        img_og (ndarray): input image
        size (int): Filter size
        line_size_1 (int): Width of filter 1
        line_size_2 (int): Width of filter 2

    Returns:
        Image after median blur
    """
    img_1 = np.copy(img_og)
    img_2 = np.copy(img_og)
    r_left_1 = int((line_size_1 - 1) / 2)
    r_right_1 = int((line_size_1 - 1) / 2) + 1
    r_left_2 = int((line_size_2 - 1) / 2)
    r_right_2 = int((line_size_2 - 1) / 2) + 1
    c_up = int((size - 1) / 2)
    c_down = int((size - 1) / 2) + 1
    for r, row in enumerate(tqdm(img_og)):
        for c, pixel in enumerate(row):
            filtered_area_1 = img_og[max(0, r-r_left_1): min(img_og.shape[0], r+r_right_1),
                            max(0, c-c_up): min(img_og.shape[0], c+c_down)]
            filtered_area_2 = img_og[max(0, r - r_left_2): min(img_og.shape[0], r + r_right_2),
                            max(0, c - c_up): min(img_og.shape[0], c + c_down)]
            img_1[r, c] = np.median(filtered_area_1)
            img_2[r, c] = np.median(filtered_area_2)
    plot_bounding_box(img_1)
    plot_bounding_box(img_2)
    return img_1 + img_2


def hist_eq(img):
    """
    Perform histogram equalization for the given image
    Args:
        img (ndarray): Input image

    Returns:
        histogram equalized image

    """
    hist, bins = np.histogram(img.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_m = np.ma.masked_equal(cdf, 0)
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')
    img2 = cdf[img]
    return img2


def apply_laplacian(src, size):
    """
    Apply laplacian transform for the given image
    Args:
        img (ndarray): Input image

    Returns:
        image after applying laplacian transform

    """
    ddepth = cv2.CV_16S
    src = cv2.GaussianBlur(src, (size, size), 0)
    # src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    dst = cv2.Laplacian(src, ddepth, ksize=size)
    abs_dst = cv2.convertScaleAbs(dst)
    return abs_dst


def edge_detection(image, sigma=0.33):
    """
    Perform canny edge detection for the given image
    Args:
        img (ndarray): Input image
        sigma
    Returns:
        image after canny edge detection

    """
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged


def subplot_img(imgs, title='Subplots'):
    """
    Subplot multiple images
    Args:
        imgs (list): List of images
        title:

    """
    fig, axes = plt.subplots(len(imgs))
    for x in range(len(imgs)):
        axes[x].imshow(imgs[x])
    plt.show()


def gaussian_blur(img, size, iterations=1):
    """
    Apply gaussian blur for given number of iterations
    Args:
        img (ndarray): Input image
        size (int): size of filter
        iterations (int): number of iterations

    Returns:
        Image after applying gaussian blur
    """
    for x in range(iterations):
        img = cv2.GaussianBlur(img, (size, size), 0)
    return img


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


# if __name__ == '__main__':
#     img = cv2.imread('/Users/anupamtripathi/PycharmProjects/Geospatial/Point_Cloud_And_Image_Misalignment/data/image/back.jpg')
#     plt.imshow(img, cmap='gray')
#     plt.show()
#     plt.imshow(zoom(img, (950, 950)), cmap='gray')
#     plt.show()
