import cv2


def apply_laplacian(src):
    ddepth = cv2.CV_16S
    # src = cv2.imread(cv2.samples.findFile(r'WhatsApp Image 2020-04-20 at 7.58.55 PM.jpeg'), cv2.IMREAD_COLOR) # Load an image
    src = cv2.resize(src, (500, 500))
    src = cv2.GaussianBlur(src, (3, 3), 0)
    print(src)
    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    print(src_gray)
    dst = cv2.Laplacian(src_gray, ddepth, ksize=3)
    print(dst)
    abs_dst = cv2.convertScaleAbs(dst)
    print(abs_dst)
    cv2.imshow('abc', abs_dst)
    cv2.waitKey(0)

    return abs_dst
