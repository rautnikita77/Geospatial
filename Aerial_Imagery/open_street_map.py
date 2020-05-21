import overpy
from Aerial_Imagery.utils import gps_to_ecef_pyproj
from PIL import Image, ImageDraw


def get_nodes(min_lat=42.051208, min_lon=-87.676717, max_lat=42.057412, max_lon=-87.668984):
    api = overpy.Overpass()
    r = api.query("way({},{},{},{}) ['highway'];(._;>;);out body;"
                  .format(min_lat, min_lon, max_lat, max_lon))
    roads = []
    for way in r.ways:
        roads.append([{'id': int(x.id), 'lat': float(x.lat), 'lon': float(x.lon),
                       'x': gps_to_ecef_pyproj([float(x.lat), float(x.lon)])[0],
                       'y': gps_to_ecef_pyproj([float(x.lat), float(x.lon)])[1]}
                      for x in way.nodes])
    return roads


(x1, y1), (x2, y2) = gps_to_ecef_pyproj([42.051208, 87.676717]), gps_to_ecef_pyproj([42.057412, 87.668984])
x_min = min(x1, x2)
y_min = min(y1, y2)
x_max = max(x1, x2)
y_max = max(y1, y2)
nodes = get_nodes()
w, h = int(x_max - x_min), int(y_max - y_min)
scale = w / (x_max - x_min)
print(w, h)
print(nodes)
shape = []
for road in nodes:
    for node1, node2 in zip(road[0:-1], road[1:]):
        shape.append([(node1['x'] - x_min) * scale,
                      (node1['y'] - y_min) * scale,
                      (node2['x'] - x_min) * scale,
                      (node2['y'] - y_min) * scale])

# shape = [(40, 40), (w - 10, h - 10)]

# creating new Image object
img = Image.new("RGB", (w, h))

print(shape)
# create line image
img1 = ImageDraw.Draw(img)
for s in shape:
    img1.line(s, fill="red", width=0)
img.show()
pass
