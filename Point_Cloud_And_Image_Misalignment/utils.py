import numpy as np
from math import cos, sin, radians
import pymap3d as pm


def lla2ecef(lat, lon, alt):
    a = 6378137
    b = 6356752.31424518
    f = (a - b)/a
    e = (f * (2 - f))**(1/2)
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

    # Rq = np.array([[1 - 2*(qy**2) - 2*(qz**2), 2*qx*qy - 2*qz*qs, 2*qx*qz + 2*qy*qs],
    #               [2*qx*qy + 2*qz*qs, 1 - 2*(qx**2) - (2*qz**2), 2*qy*qz - 2*qs*qx],
    #               [2*qx*qz - 2*qs*qy, 2*qy*qz + 2*qs*qx, 1 - 2*(qx**2) - 2*(qy**2)]])



    [[x], [y], [z]] = Rq @ np.array([[n], [e], [-u]])
    return x, y, z


def cam2image(x, y, z, Rs):
    if z > 0 and z > abs(x) and z > abs(y):
        xi = (y/z) * ((Rs - 1)/2) + ((Rs + 1)/2)
        yi = (x/z) * ((Rs - 1)/2) + ((Rs + 1)/2)
        return xi, yi
    return

