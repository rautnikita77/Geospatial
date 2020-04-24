import cv2
import os
import numpy as np
from tqdm import tqdm
import math



def load_images_from_folder(folder):
    mean_img = cv2.imread(os.path.join(folder, os.listdir(folder)[0]),0)
    print(mean_img.shape)
    for idx, filename in enumerate(tqdm(os.listdir(folder)[1:])):
        # print(idx)
        img = cv2.imread(os.path.join(folder, filename),0)
        if img is not None:
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            equ = cv2.equalizeHist(img)
            equ = img - equ
            mean_img = (mean_img * (idx + 1) + equ) / (idx + 2)
            # cv2.imwrite("temp.png", equ - img)

            # normalize float versions
            # norm_img1 = cv2.normalize(img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            # norm_img2 = cv2.normalize(gray_img, None, alpha=0, beta=4.2, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

            # scale to uint8
            # norm_img1 = (255 * norm_img1).astype(np.uint8)
            # norm_img2 = np.clip(norm_img2, 0, 1)
            # norm_img2 = (255 * norm_img2).astype(np.uint8)

            # laplacian = cv2.Laplacian(gray_img, cv2.CV_64F)

    return mean_img


def avg(img, cam):
    me =  np.mean(img, axis=0)
    cv2.imwrite(cam + "mean.png", me)
    ret, thresh1 = cv2.threshold(me, 80, 255, cv2.THRESH_BINARY)
    thresh1 = (255 - thresh1).astype(np.uint8)
    # cv2.imwrite("thresh.png", thresh1)
    #
    # circles = cv2.HoughCircles(thresh1, cv2.HOUGH_GRADIENT, dp=1, minDist=20, minRadius=0, maxRadius=0)
    # print(circles)
    # red = (0, 0, 255)
    # for x, y, r in circles[0]:
    #     cv2.circle(thresh1, (x, y), r, red, 2)

    # kernel = np.ones((10, 10), np.uint8)
    # opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)

    return (thresh1)

def main():
    # cam = 'cam_2'
    # a = load_images_from_folder(os.path.join('data', 'sample_drive', cam))
    # cv2.imwrite("mean.png", a)
    a = cv2.imread("mean.png", 0)
    a = 255 - a

    ret, thresh1 = cv2.threshold(a, 185, 255, cv2.THRESH_BINARY)
    cv2.imwrite("mean1.png", thresh1)
    # Get x-gradient in "sx"

    # Get square root of sum of squares

    # ret, thresh1 = cv2.threshold(a, 70, 255, cv2.THRESH_BINARY)


    # ret, thresh1 = cv2.threshold(a, 120, 255, cv2.THRESH_BINARY)
    # thresh1 = (255 - thresh1).astype(np.uint8)


    # a = cv2.bitwise_not(a)


    # im_with_keypoints = cv2.drawKeypoints(a, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # cv2.imwrite("keypoints.png", im_with_keypoints)

    # n = len(a)
    # img = avg(a, cam)
    # cv2.imwrite(cam+"full.png", img)
    # for i in tqdm(range(math.ceil(n/50))):
    #     img = avg(a[i:i+50:,:,:], cam)
    #     cv2.imwrite(cam+str(i)+".png", img)




if __name__ == "__main__":
    main()
    # a = [[2,1,2],[2,1,2],[2,1,2]]
    # c = [[1,2,1],[1,2,1],[1,2,1]]
    # a = np.array((a, a, a))
    # c = np.array((c, c, c))
    # b = []
    #
    # b.append(a)
    # b.append(c)
    # b = np.array(b)
    # print(np.mean(b, axis=0))
