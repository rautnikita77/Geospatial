from urllib import request
from PIL import Image
import os
from math import cos, sin, pi, log, atan, exp, floor
import math
from itertools import chain
import re

# 40.792801, -73.967553, 40.775645, -73.960642

BASEURL = 'http://ecn.t0.tiles.virtualearth.net/tiles/a{}.jpeg?g=8549'
min_lat = 41.885108
min_lon = -87.615195
max_lat = 41.893812
max_lon = -87.597778
IMAGEMAXSIZE = 8192 * 8192 * 8  # max width/height in pixels for the retrived image
TILESIZE = 256  # in Bing tile system, one tile image is in size 256 * 256 pixels


class TileSystem:

    def __init__(self):
        self.EarthRadius = 6378137
        self.MinLatitude, self.MaxLatitude = -85.05112878, 85.05112878
        self.MinLongitude, self.MaxLongitude = -180., 180.
        self.MaxLevel = 20

    def clip(self, val, minval, maxval):
        return min(max(val, minval), maxval)

    def map_size(self, level):
        return 256 << level

    def ground_resolution(self, lat, level):
        lat = self.clip(lat, self.MinLatitude, self.MaxLatitude)
        return cos(lat * pi / 180) * 2 * pi * self.EarthRadius / self.map_size(level)

    def map_scale(self, lat, level, screenDpi):
        return self.ground_resolution(lat, level) * screenDpi / 0.0254

    def latlong_to_pixelXY(self, lat, long, level):
        lat = self.clip(lat, self.MinLatitude, self.MaxLatitude)
        long = self.clip(long, self.MinLongitude, self.MaxLongitude)

        x = (long + 180) / 360
        sinlat = sin(lat * pi / 180)
        y = 0.5 - log((1 + sinlat) / (1 - sinlat)) / (4 * pi)

        mapsize = self.map_size(level)
        pixelX, pixelY = floor(self.clip(x * mapsize + 0.5, 0, mapsize - 1)), \
                         floor(self.clip(y * mapsize + 0.5, 0, mapsize - 1))
        return pixelX, pixelY

    def pixelXY_to_latlong(self, pixelX, pixelY, level):
        mapsize = self.map_size(level)
        x = self.clip(pixelX, 0, mapsize - 1) / mapsize - 0.5
        y = 0.5 - 360 * self.clip(pixelY, 0, mapsize - 1) / mapsize

        lat = 90 - 360 * atan(exp(-y * 2 * pi)) / pi
        long = 360 * x
        return lat, long

    def pixelXY_to_tileXY(self, pixelX, pixelY):
        return floor(pixelX / 256), floor(pixelY / 256)

    def tileXY_to_pixelXY(self, tileX, tileY):
        return tileX * 256, tileY * 256

    def tileXY_to_quadkey(self, tileX, tileY, level):
        tileXbits = '{0:0{1}b}'.format(tileX, level)
        tileYbits = '{0:0{1}b}'.format(tileY, level)

        quadkeybinary = ''.join(chain(*zip(tileYbits, tileXbits)))
        return ''.join([str(int(num, 2)) for num in re.findall('..?', quadkeybinary)])
        # return ''.join(i for j in zip(tileYbits, tileXbits) for i in j)

    def quadkey_to_tileXY(self, quadkey):
        quadkeybinary = ''.join(['{0:02b}'.format(int(num)) for num in quadkey])
        tileX, tileY = int(quadkeybinary[1::2], 2), int(quadkeybinary[::2], 2)
        return tileX, tileY


def horizontal_retrieval_and_stitch_image(tileX_start, tileX_end, tileY, level):
    imagelist = []
    for tileX in range(tileX_start, tileX_end + 1):
        quadkey = tile_system.tileXY_to_quadkey(tileX, tileY, level)
        with request.urlopen(BASEURL.format(quadkey)) as file:
            image = Image.open(file)

        imagelist.append(image)

    result = Image.new('RGB', (len(imagelist) * TILESIZE, TILESIZE))
    for i, image in enumerate(imagelist):
        result.paste(image, (i * TILESIZE, 0))
    return result


def main():

    for level in range(tile_system.MaxLevel, 0, -1):
        print(level)
        X1, Y1 = tile_system.latlong_to_pixelXY(min_lat, min_lon, level)
        X2, Y2 = tile_system.latlong_to_pixelXY(max_lat, max_lon, level)

        X_min, X_max = min(X1, X2), max(X1, X2)
        Y_min, Y_max = min(Y1, Y2), max(Y1, Y2)

        if abs(X1 - X2) <= 1 or abs(Y1 - Y2) <= 1:
            break

        if abs(X1 - X2) * abs(Y1 - Y2) > IMAGEMAXSIZE:
            continue

        tileX1, tileY1 = tile_system.pixelXY_to_tileXY(X_min, Y_min)
        tileX2, tileY2 = tile_system.pixelXY_to_tileXY(X_max, Y_max)

        # Stitch the tile images together
        result = Image.new('RGB', ((tileX2 - tileX1 + 1) * TILESIZE, (tileY2 - tileY1 + 1) * TILESIZE))
        retrieve_sucess = False
        for tileY in range(tileY1, tileY2 + 1):
            horizontal_image = horizontal_retrieval_and_stitch_image(tileX1, tileX2, tileY, level)
            result.paste(horizontal_image, (0, (tileY - tileY1) * TILESIZE))

        # Crop the image based on the given bounding box
        leftup_cornerX, leftup_cornerY = tile_system.tileXY_to_pixelXY(tileX1, tileY1)
        retrieve_image = result.crop((X_min - leftup_cornerX, Y_min - leftup_cornerY, \
                                      X_max - leftup_cornerX, Y_max - leftup_cornerY))
        print("Finish the aerial image retrieval at", level)
        filename = os.path.join('images', 'aerialImage_{}.jpeg'.format(level))
        retrieve_image.save(filename)

if __name__ == '__main__':
    tile_system = TileSystem()
    main()
