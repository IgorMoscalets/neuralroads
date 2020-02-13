import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import itertools
import matplotlib.image as mpimg

from lib.neuralroads import NeuralRoads

instance = NeuralRoads(path="2006chicago.json")

routes_from = instance.route_from()
routes_to = instance.route_to()
#print routes_to
#print len(routes_from)

#for x in routes_from:
#	print len(x)
#
#height = [float(routes_to[v][0]) for v in routes_to]
#bars = [str(x)[:4] for x in routes_to.keys()]

#y_pos = np.arange(len(bars))

#plt.bar(y_pos, height)

#plt.xticks(y_pos, bars)


min_latitude = instance.min_latitude()
max_latitude = instance.max_latitude()
min_longitude = instance.min_longitude()
max_longitude = instance.max_longitude()

minlat = -87.7373
maxlat = -87.6916
minlong = 41.8570
maxlong = 41.8900
"""
fig, ax = plt.subplots()

print min_longitude

routes_longitude = [routes_from[x][0]["longitude"] for x in routes_from]
routes_latitude = [routes_from[x][0]["latitude"] for x in routes_from]

ax.scatter(routes_latitude, routes_longitude, edgecolors='red', linewidths=1, zorder=2)


for i, x in enumerate(routes_to):
	if routes_to[x][0] != "ONEWAY":
		ax.annotate(str(routes_to[x][0]["volume"]), (routes_latitude[i], routes_longitude[i]))

ax.imshow(mpimg.imread('map (2).png'), extent=(maxlong, minlong, maxlat, minlat), zorder=1)

plt.show()
"""


height = [float(routes_from[v][0]["volume"]) for v in routes_from]	
bars = [str(x)[:1] for x in routes_from.keys()]

y_pos = np.arange(len(bars))

plt.bar(y_pos, height)

plt.xticks(y_pos, bars)

plt.show()
