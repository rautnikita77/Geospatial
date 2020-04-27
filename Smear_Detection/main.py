import cv2
import numpy as np
from utils import plot_bounding_box, custom_median_filter, apply_thresholding_img, dilate, median_blur, gaussian_blur
import os
from tqdm import tqdm


def detect_smear_camer(camera):
    mean = cv2.imread(os.path.join(data_path, os.listdir(data_path)[0]), cv2.IMREAD_GRAYSCALE)
    equ = cv2.equalizeHist(mean)
    mean = gaussian_blur(equ, 9)
    for n, img in enumerate(tqdm(os.listdir(data_path)[1:])):
        image = cv2.imread(os.path.join(data_path, img), cv2.IMREAD_GRAYSCALE)
        equ = cv2.equalizeHist(image)
        equ = gaussian_blur(equ, 9)
        mean = (mean * (n + 1) + equ) / (n + 2)

    mean = mean.astype(np.uint8)
    image = 255 - cv2.adaptiveThreshold(mean, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 75, 3)
    plot_bounding_box(image, title_='og camera ' + str(camera))
    lines = custom_median_filter(image, 301, 1)
    lines = dilate(lines, 3)
    plot_bounding_box(lines, title_='lines camera ' + str(camera))
    plot_bounding_box(image - lines, title_='img - lines camera ' + str(camera))

    image = image - lines
    cv2.imwrite('outputs/mask_' + str(camera) + '.jpg', image)
    image = cv2.imread('outputs/mask_' + str(camera) + '.jpg', 0)
    image = median_blur(image, 75, 1)
    image = dilate(image, 7, 7)
    image = 255 - apply_thresholding_img(image, 2, 255)
    image = dilate(image, 5, 15)
    image = median_blur(image, 51, 5)

    plot_bounding_box(image, title_='mask camera ' + str(camera))


if __name__ == "__main__":
    for camera in [2, 1, 0, 3, 5]:
        data_path = 'data/sample_drive/cam_' + str(camera)
        detect_smear_camer(camera)
