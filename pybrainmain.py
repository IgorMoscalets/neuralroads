import json

import matplotlib.pyplot as plt
import numpy as np
import itertools
import pybrain
from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import TanhLayer
from pybrain.supervised          import RPropMinusTrainer
import calendar
from datetime import datetime

with open('2006chicago.json') as dataset:
	data = json.load(dataset)
	routes_frommeasur = {}
	max_fromvol = 0.0
	max_tovol = 0.0

	for x in data:
		routes_frommeasur[str(x["Street"])] = []
	for x in data:
		date_obj = datetime.strptime(x["Date of Count"], '%m/%d/%Y')

		formaxval = float(x["Vehicle Volume By Each Direction of Traffic"].split("/")[0].split(": ")[1])
		if formaxval > max_fromvol:
			max_fromvol = formaxval

		routes_frommeasur[str(x["Street"])].append({"volume": x["Vehicle Volume By Each Direction of Traffic"].split("/")[0].split(": ")[1], "dayofweek": date_obj.weekday()})

	#print max_fromvol

	routes_tomeasur = {}
	for x in data:
		routes_tomeasur[str(x["Street"])] = []
	for x in data:
		if "Oneway" in x["Vehicle Volume By Each Direction of Traffic"]:
			routes_tomeasur[str(x["Street"])].append("ONEWAY")
		else:
			routes_tomeasur[str(x["Street"])].append(x["Vehicle Volume By Each Direction of Traffic"].split("/")[1].split(": ")[1])

	#print routes_frommeasur


	#print routes_frommeasur
	"""
	height = [float(routes_tomeasur[v][1]) for v in routes_tomeasur][1000:1030]
	bars = [str(x)[:4] for x in routes_tomeasur.keys()[1000:1030]]

	y_pos = np.arange(len(bars))

	plt.bar(y_pos, height)

	plt.xticks(y_pos, bars)

	height = [float(routes_frommeasur[v][1]) for v in routes_frommeasur][1000:1030]
	bars = [str(x)[:4] for x in routes_frommeasur.keys()[1000:1030]]

	y_pos = np.arange(len(bars))

	plt.bar(y_pos, height)

	plt.xticks(y_pos, bars)

	plt.show()
	#print routes_frommeasur
	"""

	routes_frommeasur_ids = {}
	i = 0
	for key, value in routes_frommeasur.iteritems():
		routes_frommeasur_ids[key] = i
		maxid = i + 0.0
		i+=1



	#print routes_frommeasur_ids
	
	ds = SupervisedDataSet(2, 1)

	for x in routes_frommeasur:
		#print x
		for y in routes_frommeasur[x]:
			#print y
			#print ( (routes_frommeasur_ids[x] / maxid , y["dayofweek"] / 7.0), int(y["volume"]) / max_fromvol)
			ds.addSample( (routes_frommeasur_ids[x] / maxid , y["dayofweek"] / 7.0), int(y["volume"]) / max_fromvol)
	#print "DS!!!!"
	#print ds
	
		#creating net
	net = buildNetwork(ds.indim, 3, ds.outdim, bias = True, hiddenclass=TanhLayer)

	#training net
	trainer = RPropMinusTrainer(net, verbose=True)
	trainer.trainOnDataset(ds,10)
	#trainer.testOnData(verbose=True)
	
	p = net.activate( (routes_frommeasur_ids["Halsted St"] / maxid , 3 / 7.0) )

	print p[0]
	