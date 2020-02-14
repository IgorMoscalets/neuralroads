import os, json, random
from copy import copy

from datetime import datetime

data = []

with open("datasets/2006chicagonosimu.json") as dataset:
	data_unsorted = json.load(dataset)
	data = data_unsorted
	newdata = []

	for i in range(1):
		for x in data:
			data_obj = copy(x)

			#print data_obj["Vehicle Volume By Each Direction of Traffic"]
			corrected_num = int(data_obj["Vehicle Volume By Each Direction of Traffic"].split("/")[0].split(": ")[1]) + random.randrange(-500,500,1)
			
			newstr = data_obj["Vehicle Volume By Each Direction of Traffic"].split("/")[0].split(": ")[0] + ": " + str(corrected_num) + " /" + data_obj["Vehicle Volume By Each Direction of Traffic"].split("/")[1]
			
			if "Oneway" in data_obj["Vehicle Volume By Each Direction of Traffic"]:
				newstr = newstr + " / Oneway East Bound"
			data_obj["Vehicle Volume By Each Direction of Traffic"] = newstr
			newdata.append(data_obj)
			#print x
			#print data_obj
	
	print len(newdata)

with open('datasets/2006chicago_test.json', 'w') as outfile:
    json.dump(newdata, outfile)