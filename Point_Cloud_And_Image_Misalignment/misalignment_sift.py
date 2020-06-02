import cv2
import os
import numpy as np
import random
from Point_Cloud_And_Image_Misalignment.utils import dilate

root = 'data'


def find_matching(pc, img):
    # create sift extracter to extract sift features
    sift_detector = cv2.xfeatures2d.SIFT_create()

    # Front matching
    kp1, d1 = sift_detector.detectAndCompute(pc, None)
    kp2, d2 = sift_detector.detectAndCompute(img, None)

    # create bf matcher
    bf2 = cv2.BFMatcher()

    matches = bf2.knnMatch(d1, d2, k=2)

    good1 = []
    for m, n in matches:
        if m.distance < 0.85 * n.distance:
            good1.append([m])

    matching = cv2.drawMatchesKnn(pc, kp1, img, kp2, good1, None, flags=2)
    return matching


def sample_image(img):
    sample = 4194304
    for i in range(sample):
        a, b = random.randint(0, 2047), random.randint(0, 2047)
        img[a, b] = 0
    cv2.imwrite('sampled.jpg', front_img)

    return img


if __name__ == "__main__":


    front_pc = cv2.imread(os.path.join(root, 'projections', 'front.jpg'), 0)
    front_pc = dilate(front_pc, 3, 5)
    front_img = cv2.imread(os.path.join(root, 'image', 'front.jpg'), 0)
    front_img = cv2.Canny(front_img.astype(np.uint8), 100, 600)
    back_pc = cv2.imread(os.path.join(root, 'projections', 'back.jpg'), 0)
    back_img = cv2.imread(os.path.join(root, 'image', 'back.jpg'), 0)
    back_img = cv2.Canny(back_img.astype(np.uint8), 100, 600)
    left_pc = cv2.imread(os.path.join(root, 'projections', 'left.jpg'), 0)
    left_img = cv2.imread(os.path.join(root, 'image', 'left.jpg'), 0)
    left_img = cv2.Canny(left_img.astype(np.uint8), 100, 600)
    right_pc = cv2.imread(os.path.join(root, 'projections', 'right.jpg'), 0)
    right_img = cv2.imread(os.path.join(root, 'image', 'right.jpg'), 0)
    right_img = cv2.Canny(right_img.astype(np.uint8), 100, 600)

    front_matching = find_matching(front_pc, front_img)
    back_matching = find_matching(back_pc, back_img)
    left_matching = find_matching(left_pc, left_img)
    right_matching = find_matching(right_pc, right_img)

    cv2.imwrite('data/front_matching.jpg', front_matching)
    cv2.imwrite('data/back_matching.jpg', front_matching)
    cv2.imwrite('data/left_matching.jpg', front_matching)
    cv2.imwrite('data/right_matching.jpg', front_matching)








