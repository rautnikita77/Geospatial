from urllib import request
from PIL import Image

def get_bing_map(min_lat, min_lon, max_lat, max_lon):
    """
    Returns the aerial image for the bounding box defined
    Args:
        min_lat (float): Minimum latitude
        max_lat (float): Max latitude
        min_lon (float): Minimum long
        max_lon (float): Max long

    Returns:

    """
    key = "AgVkIXYlkkwD-wKoY9IQDYy1bvLHiAaWC2ZI_LewXAfPxf-IYQeE_PLu3A9Z4ZxA"
    BASEURL = "https://dev.virtualearth.net/REST/V1/Imagery/Map/Aerial/?mapArea={},{},{},{}&key={}"\
        .format(str(min_lat), str(min_lon), str(max_lat), str(max_lon), key)

    with request.urlopen(BASEURL) as file:
        a = Image.open(file)
    a.show()
    return a


get_bing_map(min_lat=50.746, min_lon=7.154, max_lat=50.748, max_lon=7.157)
get_bing_map(min_lat=42.051208, min_lon=-87.676717, max_lat=42.057412, max_lon=-87.668984)

