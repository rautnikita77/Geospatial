import numpy as np
from math import cos, sin, radians, sqrt, pi
import pymap3d as pm
import math


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
    if z > 0 and z > abs(x) and z > abs(y):
        xi = (y/z) * ((Rs - 1)/2) + ((Rs + 1)/2)
        yi = (x/z) * ((Rs - 1)/2) + ((Rs + 1)/2)
        return xi, yi
    return


def rotate_coordinates(x, y, z, alpha, beta, gamma, degree=True):
    """
    Rotate given coordinates by angles along all axes
    Args:
        x (float): x coordinate
        y (float): y coordinate
        z (float): z coordinate
        alpha (float): Rotation along x axis
        beta (float): Rotation along y axis
        gamma (float): Rotation along z axis
        degree (bool): True if angles in degree

    Returns:
        x (float): x coordinate after rotation
        y (float): y coordinate after rotation
        z (float): z coordinate after rotation
    """
    if degree:
        alpha, beta, gamma = [math.radians(x) for x in [alpha, beta, gamma]]
    R = np.array([[cos(alpha)*cos(beta), cos(alpha)*sin(beta)*sin(gamma) - sin(alpha)*cos(gamma), cos(alpha)*sin(beta)*cos(gamma) + sin(alpha)*sin(gamma)],
                  [sin(alpha)*cos(beta), sin(alpha)*sin(beta)*sin(gamma) + cos(alpha)*cos(gamma), sin(alpha)*sin(beta)*cos(gamma) - cos(alpha)*sin(gamma)],
                  [-sin(beta), cos(beta)*sin(gamma), cos(beta)*cos(gamma)]])
    [x, y, z] = np.dot(R, np.array([[x], [y], [z]]))
    return x, y, z

