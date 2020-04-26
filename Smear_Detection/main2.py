import cv2
import os
import numpy as np
from tqdm import tqdm
import math
from utils import hist_eq, gaussian_blur, dilate, plot_bounding_box, median_blur, isolate_key_ponits



def find_mean(folder, subtract):
    mean_img = cv2.imread(os.path.join(folder, os.listdir(folder)[0]),0)

    mean_img_equ = cv2.equalizeHist(mean_img)
    mean_img_equ = cv2.equalizeHist(mean_img_equ)
    mean_img_gauss = cv2.GaussianBlur(mean_img_equ, (9, 9), 0)
    for idx, filename in enumerate(tqdm(os.listdir(folder)[1:])):
        img = cv2.imread(os.path.join(folder, filename),0)
        if img is not None:
            img_equ = cv2.equalizeHist(img)
            img_gauss = gaussian_blur(img_equ, 11, iterations=2)
            mean_img_gauss = (mean_img_gauss * (idx + 1) + img_gauss) / (idx + 2)

    return mean_img_gauss


def perform(cam, subtract=True):
    # mean = find_mean(os.path.join('data', 'sample_drive', cam), subtract)
    # cv2.imwrite("mean2.png", mean)
    mean = cv2.imread('mean5.png')

    kernel = np.ones((3, 3), np.uint8)
    bg = cv2.dilate(mean, kernel, iterations=1)
    mask = mean - bg
    cv2.imwrite("bg2.png", mask)

    for iterations in range(2):
        mask = cv2.medianBlur(mask, 101)

    plot_bounding_box(mask, 4)
    # kernel = np.ones((50, 50), np.uint8)
    # mask1 = cv2.erode(mask, kernel, iterations=1)
    # mask1 = median_blur(mask, 101, 2)
    # plot_bounding_box(mask1, 4)
    # cv2.imwrite("a.png", mask1)
    # mask = mask - mask1
    # cv2.imwrite("b.png", mask)
    plot_bounding_box(mask, 4)


    params = cv2.SimpleBlobDetector_Params()
    #
    # params.filterByArea = True
    # params.minArea = 300
    # params.maxArea = mask.shape[0] * mask.shape[1] / 2
    # #
    # params.filterByConvexity = True
    # params.minConvexity = 0.5
    # params.maxConvexity = 1

    mask = 255 - mask
    detector = cv2.SimpleBlobDetector_create(params)

    keypoints = detector.detect(mask)

    print(help(keypoints[0]))
    print(keypoints[0].convert(keypoints))

    new_mask = isolate_key_ponits(255 - mask, keypoints)

    plot_bounding_box(new_mask, -1)

    return keypoints, mask


def main():
    cam = 'cam_5'
    keypoints, mask = perform(cam)
    # if not keypoints:
    #     keypoints, mask = perform(cam, subtract = False)
    #
    print(keypoints)
    im_with_keypoints = cv2.drawKeypoints(mask, keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite('keypoints5.png', im_with_keypoints)
    cv2.imwrite('mask5.png', mask)


if __name__ == "__main__":
    main()
