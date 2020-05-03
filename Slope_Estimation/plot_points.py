import os
from numpy import genfromtxt
from Slope_Estimation.utils import plot_lat_long_points

data = 'data'

if __name__ == "__main__":
    probe = genfromtxt(os.path.join(data, 'Partition6467ProbePoints.csv'), delimiter=',')
    link = genfromtxt(os.path.join(data, 'Partition6467LinkData.csv'), delimiter=',')
    print(probe)