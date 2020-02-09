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

with open('2017trafficvolumecolorado.json') as dataset:
	data = json.load(dataset)
	routes_frommeasu = {}
	for x in data:
		routes_frommeasu[str(x["routeid"])] = []
	for x in data:
		routes_frommeasu[str(x["routeid"])].append(x["frommeasur"])

	routes_tomeasu = {}
	for x in data:
		routes_tomeasu[str(x["routeid"])] = []
	for x in data:
		routes_tomeasu[str(x["routeid"])].append(x["tomeasure"])

	routes_frommeasur = {}

	for x in routes_frommeasu:
		if len(routes_frommeasu[x]) >= 2:
			routes_frommeasur[x] = routes_frommeasu[x]

	routes_tomeasur = {}

	for x in routes_tomeasu:
		if len(routes_tomeasu[x]) >= 2:
			routes_tomeasur[x] = routes_tomeasu[x]

	print len(routes_frommeasur)

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
		i+=1
	#print routes_frommeasur_ids

	ds = SupervisedDataSet(1, 1)

	for x in routes_frommeasur:
		#print x
		for y in routes_frommeasur[x]:
			#print y
			ds.addSample( routes_frommeasur_ids[x] , y)


	#code for normalize data in ds
	i = np.array([d[0] for d in ds])
	inorm = np.array([d[0] for d in ds])
	i /= np.max(np.abs(i),axis=0)
	o = np.array([d[1] for d in ds])
	onorm = np.array([d[1] for d in ds])
	o /= np.max(np.abs(o),axis=0)

	print routes_frommeasur_ids["11000602"] / np.max(np.abs(inorm),axis=0)
	#creating new object for normalized data
	nds = SupervisedDataSet(1, 1)
	for ix in range(len(ds)):
		nds.addSample( i[ix], o[ix])
	#print routes_frommeasur
	
		#creating net
	net = buildNetwork(nds.indim, 3, nds.outdim, bias = True, hiddenclass=TanhLayer)

	#training net
	trainer = RPropMinusTrainer(net, verbose=True)
	trainer.trainOnDataset(nds,10)
	#trainer.testOnData(verbose=True)
	
	p = net.activate( routes_frommeasur_ids["11000602"] / np.max(np.abs(inorm),axis=0))

	print (p[0]*np.max(np.abs(onorm),axis=0)[0])