import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from lib.neuralroads import NeuralRoads
import json

from datetime import datetime

import keras

instance = NeuralRoads(path="2006chicago.json")

instance_test = NeuralRoads(path="2006chicago_test.json")


max_fromvol = instance.max_fromvolume()
routes_frommeasur = instance.route_from()

routes_frommeasur_ids = {}

maxid = 0

i = 0
for key, value in routes_frommeasur.iteritems():
	routes_frommeasur_ids[key] = i
	maxid = i + 0.0
	i+=1

routes_frommeasur_ids_arr = {}

b = 0
for key, value in routes_frommeasur.iteritems():
	#print key
	routes_frommeasur_ids_arr[key] = np.zeros(int(maxid+1))	
	routes_frommeasur_ids_arr[key][b] = 1
	#print routes_frommeasur_ids_arr[key]
	b+=1

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

		x1n.append(routes_frommeasur_ids_arr[x])
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

print x1.shape, "SHAPE X1"

model = keras.Sequential([keras.layers.Dense(units=1, input_shape=[1203])])
model.compile(optimizer='sgd', loss='mean_squared_error')
model.fit(x1,y1, batch_size=4, epochs=100)

print len(x1)

test_data = instance_test.get_test_data_sorted()

testspl = 0
total = 0

prediction_set = {}

for x in test_data:
	test_volume = x["Vehicle Volume By Each Direction of Traffic"].split("/")[0].split(": ")[1]
	test_route_name = x["Traffic Volume Count Location  Address"]
	test_street = x["Street"]
	test_route_id = routes_frommeasur_ids[test_route_name]
	test_route_id_arr = np.zeros(int(maxid+1))
	test_route_id_arr[test_route_id] = 1
	#print len(test_route_id_arr), " ID ARR"
	date_obj = datetime.strptime(x["Date of Count"], '%m/%d/%Y')
	test_weekday = date_obj.weekday()
	total += 1
	# 	print test_weekday, "Week Day"
	# 	print test_volume
	# 	print test_route_name
	# 	print test_route_id

	#print test_route_id_arr.shape, " SHAPE ARR"

	predictn = model.predict([[test_route_id_arr]])[0] * max_fromvol
	#print predictn, "- prediction, ", test_volume, "- real information"
	if not ( float(predictn) > float(test_volume) + 2000 or float(predictn) < float(test_volume) - 2000 ):
		testspl += 1
	prediction_set[x["Traffic Volume Count Location  Address"]] = int(predictn)

print prediction_set
with open('trained_data.json', 'w') as outfile:
    json.dump(prediction_set, outfile)

print testspl, " / ", total, ": ", float(testspl)/float(total)*100. 
