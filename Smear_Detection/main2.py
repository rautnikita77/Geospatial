import cv2
import os
import numpy as np
from tqdm import tqdm
import math
from utils import hist_eq, plot_bounding_box, gaussian_blur, dilate



def load_images_from_folder(folder):
    mean_img = cv2.imread(os.path.join(folder, os.listdir(folder)[0]),0)
    mean_img_equ = cv2.equalizeHist(mean_img)
    mean_img_equ = mean_img - mean_img_equ
    mean_img_gauss = cv2.GaussianBlur(mean_img_equ, (9, 9), 0)
    for idx, filename in enumerate(tqdm(os.listdir(folder)[1:])):
        img = cv2.imread(os.path.join(folder, filename),0)
        if img is not None:
            img_equ = cv2.equalizeHist(img)
            img_equ = img - img_equ
            img_gauss = gaussian_blur(img_equ, 11, iterations=2)
            mean_img_gauss = (mean_img_gauss * (idx + 1) + img_gauss) / (idx + 2)

    return mean_img_gauss



def main():
    cam = 'cam_2'
    mean = load_images_from_folder(os.path.join('data', 'sample_drive', cam))
    cv2.imwrite("mean.png", mean)
    mean = cv2.imread('mean.png', 0)

    kernel = np.ones((3, 3), np.uint8)
    bg = cv2.dilate(mean, kernel, iterations=1)
    mask = mean - bg
    cv2.imwrite("bg.png", mask)

    for iterations in range(1):
        mask = cv2.medianBlur(mask,101)
        cv2.imwrite(str(iterations) + 'bg.png', mask)

    params = cv2.SimpleBlobDetector_Params()

    params.filterByArea = True
    params.minArea = 3
    params.maxArea = 1023 * 1023

    mask = 255 - mask
    detector = cv2.SimpleBlobDetector_create(params)

    keypoints = detector.detect(mask)
    im_with_keypoints = cv2.drawKeypoints(mask, keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imwrite('keypoints.png', im_with_keypoints)
    cv2.imwrite('mask.png', mask)



if __name__ == "__main__":
    main()
