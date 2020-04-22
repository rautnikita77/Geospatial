import cv2
from matplotlib import pyplot as plt
import numpy as np
from utils import apply_laplacian, hist_eq, subplot_img, plot_cam2_bounding_box, apply_thresholding_img
import os
from tqdm import tqdm


data_path = '/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/data/sample_drive/cam_2'


def create_smear_mask(img):
    img_hist_eq = hist_eq(img)
    og_hist = img - img_hist_eq
    og_hist = (og_hist * (255 / np.max(og_hist))).astype(np.float32)
    og_hist_gray = cv2.cvtColor(og_hist, cv2.COLOR_BGR2GRAY)
    print(np.unique(og_hist_gray))
    hist_threshold = apply_thresholding_img(og_hist_gray, 100, 250)
    return hist_threshold


if __name__ == "__main__":
    masks = []
    sum_ = 0
    for n, img in tqdm(enumerate(os.listdir(data_path))):
        image = cv2.imread(os.path.join(data_path, img))
        mask = create_smear_mask(image)
        if isinstance(sum_, int):
            sum_ = mask
        else:
            sum_ += mask
        # masks.append(mask)
        # print(np.unique(mask))
        # plt.imshow(mask)
        # plt.show()
        # # break
        # subplot_img([image, mask])
        plot_cam2_bounding_box(mask.astype(np.float32))
        if n == 5:
            break

    # plt.imshow(sum_)
    # plt.imshow(sum_)
    # plt.show()

    #
    # masks = np.array(masks)
    # masks_mean = np.mean(masks, axis=0)
    # plt.imshow(masks_mean)
    # plt.show()
