import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from lib.neuralroads import NeuralRoads

from datetime import datetime

import keras

instance = NeuralRoads(path="2006chicago.json")


max_fromvol = instance.max_fromvolume()
routes_frommeasur = instance.route_from()

routes_frommeasur_ids = {}

maxid = 0

i = 0
for key, value in routes_frommeasur.iteritems():
	routes_frommeasur_ids[key] = i
	maxid = i + 0.0
	i+=1

routes_frommeasur_streetid = {}

j = 0

maxstreetid = 0

for x in routes_frommeasur:
	for z in routes_frommeasur[x]:
		if z["street"] not in routes_frommeasur_streetid:
			routes_frommeasur_streetid[z["street"]] = j
			maxstreetid = j + 0.0
			j+=1
# print routes_frommeasur_streetid

#for x in routes_frommeasur:
	#print len(routes_frommeasur[x])

#print routes_frommeasur_ids

x1n = []
x2n = []
x3n = []

y1n = []

for x in routes_frommeasur:
	#print x
	for y in routes_frommeasur[x]:
		#print y
		#print ( (routes_frommeasur_ids[x] / maxid , y["dayofweek"] / 7.0), int(y["volume"]) / max_fromvol)

		x1n.append(routes_frommeasur_ids[x] / maxid)
		x2n.append(y["dayofweek"] / 7.0)
		x3n.append(routes_frommeasur_streetid[y["street"]] / maxstreetid)
		y1n.append(int(y["volume"]) / max_fromvol)
		#ds.addSample( (routes_frommeasur_ids[x] / maxid , y["dayofweek"] / 7.0), int(y["volume"]) / max_fromvol)
#print "DS!!!!"
#print ds
#print y1n
x1 = np.array(x1n)
x2 = np.array(x2n)
x3 = np.array(x3n)
y1 = np.array(y1n)

#print routes_frommeasur_ids
merged_array = np.stack([x1, x2, x3], axis=1)

model = keras.Sequential([
keras.layers.Dense(64, input_dim=3, activation=keras.activations.relu),
keras.layers.Dense(64, activation=keras.activations.relu),
keras.layers.Dense(1)
])


model.compile(optimizer='rmsprop', loss='mean_squared_error')
model.fit(merged_array,y1, batch_size=16, epochs=1000)

print x1

test_data = instance.get_test_data_sorted()

testspl = 0
total = 0

for x in test_data:
	test_volume = x["Vehicle Volume By Each Direction of Traffic"].split("/")[0].split(": ")[1]
	test_route_name = x["Traffic Volume Count Location  Address"]
	test_street = x["Street"]
	test_route_id = routes_frommeasur_ids[test_route_name]
	date_obj = datetime.strptime(x["Date of Count"], '%m/%d/%Y')
	test_weekday = date_obj.weekday()
	total += 1
	# 	print test_weekday, "Week Day"
	# 	print test_volume
	# 	print test_route_name
	# 	print test_route_id

	predictn = (model.predict(np.array([(test_route_id/maxid, test_weekday/7, routes_frommeasur_streetid[test_street] / maxstreetid)])) * max_fromvol)[0]
	print predictn, "- prediction, ", test_volume, "- real information"
	if not ( float(predictn) > float(test_volume) + 2000 or float(predictn) < float(test_volume) - 2000 ):
		testspl += 1

print testspl, " / ", total, ": ", testspl/total*100. 