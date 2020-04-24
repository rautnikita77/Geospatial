import cv2
from matplotlib import pyplot as plt
import numpy as np
from utils import hist_eq, plot_cam2_bounding_box, gaussian_blur, dilate
import os
from tqdm import tqdm

camera = 3
data_path = '/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/data/sample_drive/cam_' + str(camera)


def create_smear_mask(img):
    # plot_cam2_bounding_box(img, 'og')
    img_hist_eq = hist_eq(img)
    plot_cam2_bounding_box(img_hist_eq, 'hist eq')
    og_hist = img_hist_eq - img
    og_hist = (og_hist * (255 / np.max(og_hist))).astype(np.float32)
    plot_cam2_bounding_box(og_hist, 'hist_eq - img col')
    og_hist_gray = cv2.cvtColor(og_hist, cv2.COLOR_BGR2GRAY)
    plot_cam2_bounding_box(og_hist_gray, 'hist_eq - img')
    # hist_threshold = apply_thresholding_img(og_hist_gray, 170, 240)
    # plot_cam2_bounding_box(hist_threshold.astype(np.float32), 'hist_eq - img')
    return og_hist_gray


if __name__ == "__main__":
    mean = []
    for n, img in tqdm(enumerate(os.listdir(data_path))):
        image = cv2.imread(os.path.join(data_path, img), cv2.IMREAD_GRAYSCALE)
        img_hist = hist_eq(image)
        img_gauss = gaussian_blur(img_hist, 10)
        mean.append(img_gauss)

    mean = np.array(mean)
    mean = np.mean(mean, axis=0)
    print(mean.dtype)
    cv2.imwrite('test3.jpg', mean)
    mean = cv2.imread('test3.jpg')
    plot_cam2_bounding_box(mean, camera, 'Mean camera ' + str(camera))
    kernel = np.ones((3, 3), np.uint8)
    bg = cv2.dilate(mean, kernel, iterations=1)
    plot_cam2_bounding_box(mean - bg, camera, 'BG ' + str(camera))
    mask = mean - bg
    print(mask.dtype, np.max(mask))
    for iterations in range(2):
        mask = cv2.medianBlur(mask, 101)
    plot_cam2_bounding_box(mask, camera, 'Mask camera ' + str(camera))
