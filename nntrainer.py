from databaseObject import *

from pybrain.datasets import SupervisedDataSet
from pybrain.supervised import BackpropTrainer
import pickle

class NNTrainer:
	def __init__(self):
		print("Created")

	def createDataset(self, fields, successField, dataType):
		data = SupervisedDataSet(len(fields),1)

		db = Database();

		fields.append(successField)
		newArr = db.getFields(fields, dataType)

		for row in newArr:
			arr = []

			for field in fields:
				if (field != successField):
					arr.append(row[field]);

			# add sample to set
			data.addSample(arr,row[successField])

		fields.pop()

		return data;

	def trainNetwork(self, net, dataset):
		t = BackpropTrainer(net, dataset, learningrate = 0.01, momentum = 0.99, verbose = False)
		t.train()
		return t

	def exportObj(self, exportObj, filename):
		exportFile = open(filename, 'w')
		pickle.dump(exportObj, exportFile)

	def importObj(self, filename):
		importFile = open(filename,'r')
		importObj = pickle.load(importFile)
		return importObj