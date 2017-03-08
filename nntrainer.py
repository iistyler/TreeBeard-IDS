from databaseObject import *

from pybrain.datasets import SupervisedDataSet
from pybrain.supervised import BackpropTrainer
import pickle

class NNTrainer:
	def __init__(self):
		print("Created")

	def createDataset(self, fields, successField):
		data = SupervisedDataSet(len(fields),1)

		db = Database();

		fields.append(successField)
		newArr = db.getFields(fields, "test", None)

		# Get each row from DB
		for row in newArr:
			arr = []

			# Append each field to dataset
			for field in fields:
				if (field != successField):
					arr.append(row[field]);

			# Add sample to set
			data.addSample(arr,row[successField])

		# Remve the success field
		fields.pop()

		return data;

	def trainNetwork(self, net, dataset):
		t = BackpropTrainer(net, dataset, learningrate = 0.01, momentum = 0.99, verbose = False)
		t.train()
		return t

	def exportObj(self, exportObj, filename):
		# Save any object to a file
		exportFile = open(filename, 'w')
		pickle.dump(exportObj, exportFile)

	def importObj(self, filename):
		# Import any object from a file
		importFile = open(filename,'r')
		importObj = pickle.load(importFile)
		return importObj
