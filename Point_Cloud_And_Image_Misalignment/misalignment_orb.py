import cv2
import os
import numpy as np
import random
from Point_Cloud_And_Image_Misalignment.utils import dilate, zoom_out

root = 'data'


def find_matching(pc, img):
    # Create ORB detector with 5000 features.
    orb_detector = cv2.ORB_create(1500)

    # Find keypoints and descriptors.
    kp1, d1 = orb_detector.detectAndCompute(pc, None)
    kp2, d2 = orb_detector.detectAndCompute(img, None)

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match the two sets of descriptors.
    matches = matcher.match(d1, d2)
    # Sort matches on the basis of their Hamming distance.
    matches.sort(key=lambda x: x.distance)

    matching = cv2.drawMatches(pc, kp1, img, kp2, matches[:50], None, flags=2)

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
    front_pc = dilate(front_pc, 3,5)
    ret, front_pc = cv2.threshold(front_pc, 50, 255, cv2.THRESH_BINARY)
    front_img = cv2.imread(os.path.join(root, 'image', 'front.jpg'), 0)
    ret, thresh1 = cv2.threshold(front_img, 200, 255, cv2.THRESH_BINARY)
    cv2.imwrite('data/a.jpg', thresh1)
    cv2.imwrite('data/c.jpg', front_pc)

    loss = np.sum((thresh1 - front_pc ** 2))
    print(loss)

    rows, cols = front_pc.shape
    M = np.float32([[1, 0, 10], [0, 1, -10]])
    front_pc = cv2.warpAffine(front_pc, M, (cols, rows))

    front_pc = zoom_out(front_pc, (front_pc.shape[0] - 50, front_pc.shape[1] - 50))
    cv2.imwrite('data/b.jpg', front_pc)

    loss = np.sum((thresh1[25:-25, 25:-25] - front_pc[25:-25, 25:-25]) ** 2)
    print(loss/((rows - 50) * (cols - 50)))
    # cv2.waitKey(0)

    # front_img = cv2.Canny(front_img.astype(np.uint8), 100, 600)
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








