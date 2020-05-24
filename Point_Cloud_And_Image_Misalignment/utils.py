import numpy as np


def enu2cam(e, n, u, qs, qx, qy, qz):
    Rq = np.array([[qs**2 + qx**2 - qy**2 - qz**2, 2*qx*qy - 2*qs*qz, 2*qx*qz + 2*qs*qy],
                  [2*qx*qy + 2*qs*qz, qs**2 - qx**2 + qy**2 - qz**2, 2*qy*qz - 2*qs*qx],
                  [2*qx*qz - 2*qs*qy, 2*qy*qz + 2*qs*qx, qs**2 - qx**2 - qy**2 + qz**2]])

    [x, y, z] = Rq @ [n, e, -u]
    return x, y, z


def cam2image(x, y, z, Rs):
    if z > 0 and z > abs(x) and z > abs(y):
        xi = (y/z) * ((Rs - 1)/2) + ((Rs + 1)/2)
        yi = (x/z) * ((Rs - 1)/2) + ((Rs + 1)/2)
        return xi, yi
    return

