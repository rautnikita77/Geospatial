import cv2
from matplotlib import pyplot as plt
import numpy as np
from utils import apply_laplacian, hist_eq, subplot_img, plot_cam2_bounding_box, apply_thresholding_img
import os
from tqdm import tqdm


data_path = '/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/data/sample_drive/cam_3'


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
    masks = []
    sum_ = 0
    for n, img in tqdm(enumerate(os.listdir(data_path))):
        image = cv2.imread(os.path.join(data_path, img))
        # image = cv2.imread('/Users/anupamtripathi/PycharmProjects/Geospatial/Smear_Detection/data/sample_drive/cam_2/393412416.jpg')
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
        # plot_cam2_bounding_box(mask.astype(np.float32))
        # if n == 50:
        #     break
        # break
        if n == 3:
            break

    # plt.imshow(sum_)
    # plt.title('Sum')
    # # plt.imshow(sum_)
    # plt.show()
    # temp = sum_ - 120000
    # temp = temp / np.max(temp)
    temp = sum_
    temp = sum_ - np.max(temp) + 1000
    temp = temp / np.max(temp)
    plot_cam2_bounding_box(sum_)
    plot_cam2_bounding_box(temp * 255)

    #
    # masks = np.array(masks)
    # masks_mean = np.mean(masks, axis=0)
    # plt.imshow(masks_mean)
    # plt.show()
