import numpy as np
from math import cos, sin, radians, sqrt, pi
import pymap3d as pm
import math
import cv2


def lla2ecef(lat, lon, alt):
    a = 6378137.0
    b = 6356752.314245
    f = (a - b)/a
    e = sqrt(f*(2-f))
    lat = radians(lat)
    lon = radians(lon)
    N = a / (1 - ((e**2) * sin(lat)**2))**(1/2)
    x = (alt + N) * cos(lon) * cos(lat)
    y = (alt + N) * cos(lat) * sin(lon)
    z = (alt + N * (1 - e**2)) * sin(lat)
    return x, y, z


def ecef2enu(x, y, z, lat0, lon0, alt0):
    x0, y0, z0 = lla2ecef(lat0, lon0, alt0)
    R = np.array([[-sin(radians(lon0)), cos(radians(lon0)), 0],
                  [-cos(radians(lon0)) * sin(radians(lat0)), -sin(radians(lat0)) * sin(radians(lon0)), cos(radians(lat0))],
                  [cos(radians(lat0)) * cos(radians(lon0)), cos(radians(lat0)) * sin(radians(lon0)), sin(radians(lat0))]])

    [[e], [n], [u]] = R @ np.array([[x - x0], [y - y0], [z - z0]])
    return e, n, u


def enu2cam(e, n, u, qs, qx, qy, qz):
    # Rq = np.array([[qs**2 + qx**2 - qy**2 - qz**2, 2*qx*qy - 2*qs*qz, 2*qx*qz + 2*qs*qy],
    #               [2*qx*qy + 2*qs*qz, qs**2 - qx**2 + qy**2 - qz**2, 2*qy*qz - 2*qs*qx],
    #               [2*qx*qz - 2*qs*qy, 2*qy*qz + 2*qs*qx, qs**2 - qx**2 - qy**2 + qz**2]])

    Rq = np.array([[1 - 2*qy**2 - 2*qz**2, 2*qx*qy - 2*qz*qs, 2*qx*qz + 2*qy*qs],
                  [2*qx*qy + 2*qz*qs, 1 - 2*qx**2 - 2*qz**2, 2*qy*qz - 2*qs*qx],
                  [2*qx*qz - 2*qs*qy, 2*qy*qz + 2*qs*qx, 1 - 2*qx**2 - 2*qy**2]])

    [[x], [y], [z]] = Rq @ np.array([[n], [e], [-u]])
    return x, y, z


def cam2image(x, y, z, Rs):

    xi = (y/z) * ((Rs - 1)/2) + ((Rs + 1)/2)
    yi = (x/z) * ((Rs - 1)/2) + ((Rs + 1)/2)
    return xi.int(), yi.int()


def dilate(img, size, iterations=1):
    """
    Apply binary dilation to image for given number of iterations
    Args:
        img (ndarray): input image
        size (int): Filter size
        iterations (int): Number of iterations

    Returns:
        Image after dilation
    """
    kernel = np.ones((size, size), np.uint8)
    bg = cv2.dilate(img, kernel, iterations=iterations)
    return bg


def erode(img, size, iterations=1):
    """
    Apply erosion to image for given number of iterations
    Args:
        img (ndarray): input image
        size (int): Filter size
        iterations (int): Number of iterations

    Returns:
        Image after erosion
    """
    kernel = np.ones((size, size), np.uint8)
    bg = cv2.erode(img, kernel, iterations=iterations)
    return bg


def median_blur(img, size, iterations=1):
    """
    Apply median blur to image for given number of iterations
    Args:
        img (ndarray): input image
        size (int): Filter size
        iterations (int): Number of iterations

    Returns:
        Image after median blur
    """
    for iterations in range(iterations):
        img = cv2.medianBlur(img, size)
    return img


def zoom_out(img, size):
    """
    Zoom out given images without changing the size
    Args:
        img (ndarray): image to be zoomed out
        size (tuple): size of desired zoomed out image

    Returns:

    """
    new_img = np.zeros_like(img)
    img = cv2.resize(img, size)
    new_img[int(new_img.shape[0]/2) - int(img.shape[0]/2): int(new_img.shape[0]/2) + int(img.shape[0]/2),
    int(new_img.shape[1]/2) - int(img.shape[1]/2): int(new_img.shape[1]/2) + int(img.shape[1]/2)] = img
    return new_img
