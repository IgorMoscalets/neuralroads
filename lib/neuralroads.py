
import os, json
from datetime import datetime

class NeuralRoads():

	def __init__(self, *args, **kwargs):
		print "Neural Roads activated !"

		self.PATH = "../datasets/"

		if (kwargs.get("path")):

			self.PATH = "datasets/" + kwargs.get("path")

		with open(self.PATH) as dataset:
			data_unsorted = json.load(dataset)
			data_all = sorted(data_unsorted,
				key=lambda x: datetime.strptime(x['Date of Count'], '%m/%d/%Y'))
			data = data_all

			self.data_test = data_all[1000:]

			self.data_sorted = data

			self.routes_frommeasur = {}
			max_fromvol = 0.0
			max_tovol = 0.0
			for x in data:
				self.routes_frommeasur[str(x["Traffic Volume Count Location  Address"])] = []
			for x in data:
				date_obj = datetime.strptime(x["Date of Count"], '%m/%d/%Y')
				# print x["Date of Count"]

				formaxval = float(x["Vehicle Volume By Each Direction of Traffic"].split("/")[0].split(": ")[1])
				if formaxval > max_fromvol:
					max_fromvol = formaxval

				self.routes_frommeasur[str(x["Traffic Volume Count Location  Address"])].append(
					{"volume": x["Vehicle Volume By Each Direction of Traffic"].split("/")[0].split(": ")[1],
					 "dayofweek": date_obj.weekday(),
					 "street": str(x["Street"]),
					 "latitude": float(x["Latitude"]),
					 "longitude": float(x["Longitude"])})

			self.routes_tomeasur = {}
			for x in data:
				self.routes_tomeasur[str(x["Traffic Volume Count Location  Address"])] = []
			for x in data:
				date_obj = datetime.strptime(x["Date of Count"], '%m/%d/%Y')

				if "Oneway" in x["Vehicle Volume By Each Direction of Traffic"]:
					self.routes_tomeasur[str(x["Traffic Volume Count Location  Address"])].append("ONEWAY")
				else:
					self.routes_tomeasur[str(x["Traffic Volume Count Location  Address"])].append(
						{"volume": x["Vehicle Volume By Each Direction of Traffic"].split("/")[1].split(": ")[1],
						"dayofweek": date_obj.weekday(),
						"street": str(x["Street"])})
			self.maxfromvol = max_fromvol


	def route_from(self):
		return self.routes_frommeasur

	def route_to(self):
		return self.routes_tomeasur

	def min_latitude(self):
		latitude_arr = [x["Latitude"] for x in self.data_sorted]
		return min(latitude_arr)

	def max_latitude(self):
		latitude_arr = [x["Latitude"] for x in self.data_sorted]
		return max(latitude_arr)

	def min_longitude(self):
		longitude_arr = [x["Longitude"] for x in self.data_sorted]
		return min(longitude_arr)

	def max_longitude(self):
		longitude_arr = [x["Longitude"] for x in self.data_sorted]
		return max(longitude_arr)

	def max_fromvolume(self):
		return self.maxfromvol

	def get_test_data_sorted(self):
		return self.data_test