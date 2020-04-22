import cv2
from matplotlib import pyplot as plt
import numpy as np
from utils import apply_laplacian, hist_eq
import os
from tqdm import tqdm


data_path = '/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/data/sample_drive/cam_2'


def create_smear_mask(img):
    img_hist_eq = hist_eq(img)
    og_hist = img - img_hist_eq
    og_hist_gray = cv2.cvtColor(og_hist, cv2.COLOR_BGR2GRAY)
    hist_threshold = np.where(og_hist_gray > 200, 0, 255)
    return hist_threshold


if __name__ == "__main__":
    masks = []
    for n, img in tqdm(enumerate(os.listdir(data_path))):
        image = cv2.imread(os.path.join(data_path, img))
        mask = create_smear_mask(image)
        # masks.append(mask)
        plt.imshow(mask)
        plt.show()
        # break
        if n == 10:
            break
    #
    # masks = np.array(masks)
    # masks_mean = np.mean(masks, axis=0)
    # plt.imshow(masks_mean)
    # plt.show()
