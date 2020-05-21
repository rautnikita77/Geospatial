from PIL import Image
import osmnx as ox
import numpy as np


# Defining the map boundaries 42.051208, min_lon=-87.676717, max_lat=42.057412, max_lon=
north, east, south, west = 42.057412, -87.668984, 42.051208, -87.676717
# Downloading the map as a graph object
G = ox.graph_from_bbox(north, south, east, west, network_type='all', retain_all=True)
# Plotting the map graph
ox.plot_graph(G, node_size=0, bgcolor='white', save=True, edge_color='#FF0000')


aerial = Image.open('images/aerialImage_20.jpeg')
aerial = aerial.convert("RGBA")
img = Image.open('images/temp.png')
datas = img.getdata()

newData = []
for item in datas:
    if item[0] == 255 and item[1] == 255 and item[2] == 255:
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)

img.putdata(newData)

baseheight = aerial.size[1]
hpercent = (baseheight/float(img.size[1]))
wsize = int((float(img.size[0])*float(hpercent)))
img = img.resize((wsize, baseheight), Image.ANTIALIAS)


aerial.paste(img, (0,0), img)
aerial.save("images/overlayed.png", "PNG")
aerial.show()
print(np.array(img).shape)
print(np.array(aerial).shape)





