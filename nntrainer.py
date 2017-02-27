from nnobject import *
from databaseObject import *

from pybrain.datasets import SupervisedDataSet
from pybrain.supervised import BackpropTrainer

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

		return data;

	def trainNetwork(self, numRuns, net, dataset):
		t = BackpropTrainer(net, dataset, learningrate = 0.01, momentum = 0.99, verbose = False)
		for epoch in range(0, numRuns):
			t.train()
		return t