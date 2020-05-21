"""
Bing API key: AgVkIXYlkkwD-wKoY9IQDYy1bvLHiAaWC2ZI_LewXAfPxf-IYQeE_PLu3A9Z4ZxA
"""
import pyproj


def gps_to_ecef_pyproj(lat_long_alt):
    """
    Convert gps lat long alt coordinates to ecef
    Args:
        lat_long_alt (list): lat, long, alt

    Returns:
        x, y, z: ecef coordinates

    """
    if len(lat_long_alt) == 3:
        ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
        lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
        x, y, z = pyproj.transform(lla, ecef, lat_long_alt[0], lat_long_alt[1], lat_long_alt[2], radians=False)
        return (x, y, z)
    else:
        ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
        lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
        x, y = pyproj.transform(lla, ecef, lat_long_alt[0], lat_long_alt[1], radians=False)
        return (x, y)


if __name__ == "__main__":
    print(gps_to_ecef_pyproj([50.746, 7.154]))
    print(gps_to_ecef_pyproj([50.7468739, 7.1563067]))
    print(gps_to_ecef_pyproj([50.748, 7.157]))
