import json

import matplotlib.pyplot as plt
import numpy as np
import itertools

import pathlib

import pandas as pd
import seaborn as sns

from lib.neuralroads import NeuralRoads
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

import calendar
from datetime import datetime


	#print routes_frommeasur


	#print routes_frommeasur
	"""
	height = [float(routes_tomeasur[v][0]) for v in routes_tomeasur]
	bars = [str(x)[:4] for x in routes_tomeasur.keys()]

	y_pos = np.arange(len(bars))

	plt.bar(y_pos, height)

	plt.xticks(y_pos, bars)
	"""
	height = [float(routes_frommeasur[v][0]["volume"]) for v in routes_frommeasur]
	bars = [str(x)[:0] for x in routes_frommeasur.keys()]

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
	"""