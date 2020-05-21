# import requests
# from bs4 import BeautifulSoup
# from urllib import request
# from PIL import Image
#
# def get_bing_map(min_lat, max_lat, min_lon, max_lon):
#     """
#     Returns the aerial image for the bounding box defined
#     Args:
#         min_lat (float): Minimum latitude
#         max_lat (float): Max latitude
#         min_lon (float): Minimum long
#         max_lon (float): Max long
#
#     Returns:
#
#     """
#     key = "AgVkIXYlkkwD-wKoY9IQDYy1bvLHiAaWC2ZI_LewXAfPxf-IYQeE_PLu3A9Z4ZxA"
#     # BASEURL = "https://dev.virtualearth.net/REST/V1/Imagery/Map/Aerial/?mapArea={},{},{},{}&mapSize=2000,1500&key={}"\
#     #     .format(str(min_lat), str(max_lat), str(min_lon), str(max_lon), key)
#
#     BASEURL = "https://api.openstreetmap.org/api/0.6/map?bbox=11.54,48.14,11.543,48.145"
#     with request.urlopen(BASEURL) as file:
#         a = Image.open(file)
#     print(a)
#     a.show()
#     return a
#
#
# get_bing_map(37.317227, -122.318439, 37.939081, -122.194565)

import networkx as nx
import overpy
import matplotlib.pyplot as plt
import numpy as np

# api = overpy.Overpass()
# r = api.query("""
# way(50.746,7.154,50.748,7.157) ["highway"];
#     (._;>;);
#     out body;
# """)
#
# # print(r.ways)
# links = []
# for way in r.ways:
#     link = []
#     # print(way.nodes)
#     for node in way.nodes:
#         link.append([float(node.lat), float(node.lon)])
#     links.append(link)
#
# print(links)
# links = np.array(links)
import osmnx as ox
# Defining the map boundaries
north, east, south, west = 33.798, -84.378, 33.763, -84.422
# Downloading the map as a graph object
G = ox.graph_from_bbox(north, south, east, west, network_type = 'drive')
# Plotting the map graph
ox.plot_graph(G, node_size=0)

