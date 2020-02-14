import json
from lib.neuralroads import NeuralRoads


instance = NeuralRoads(path="2006chicagonosimu.json")

data = instance.route_from()

with open('dotsweb.json', 'w') as outfile:
    json.dump(data, outfile)