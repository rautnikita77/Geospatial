import requests
from bs4 import BeautifulSoup
from urllib import request
from PIL import Image

def get_bing_map(min_lat, max_lat, min_lon, max_lon):
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
    BASEURL = "https://dev.virtualearth.net/REST/V1/Imagery/Map/Aerial/?mapArea={},{},{},{}&mapSize=2000,1500&key={}"\
        .format(str(min_lat), str(max_lat), str(min_lon), str(max_lon), key)

    with request.urlopen(BASEURL) as file:
        a = Image.open(file)
    print(a)
    a.show()
    return a


get_bing_map(37.317227, -122.318439, 37.939081, -122.194565)


