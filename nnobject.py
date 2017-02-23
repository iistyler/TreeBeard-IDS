import json
from pprint import pprint

class NNObject:
	def __init__(self, file):

		with open('JSONNetDesc/exampleNetwork') as data_file:    
			data = json.load(data_file)

		self.name = data["name"]
		self.hiddenLayers = data["hiddenLayers"]
		self.input = data["input"]