from databaseObject import *

from pybrain.datasets import SupervisedDataSet
from pybrain.supervised import BackpropTrainer
import pickle
from time import gmtime, strftime

class NNTrainer:
	def __init__(self):
		print("Created")

	def createDataset(self, fields, successField, typeRuns, normRuns):
		data = SupervisedDataSet(len(fields),1)

		db = Database();

		fields.append(successField)
		newArr = []

		if (successField != "normal"):
			for x in range(normRuns):
				# print "Ran norm"
				newArr += db.getFields(fields, "train", None, None)
			for x in range(typeRuns):
				# print "Ran type " + successField
				newArr += db.getFields(fields, "train", None, successField)
		else:
			for x in range(typeRuns):
				# print "Ran norm"
				newArr += db.getFields(fields, "train", None, "normal")
			for x in range(normRuns):
				# print "Ran all"
				newArr += db.getFields(fields, "train", None, None)

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
		print("Started Training: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))

		t = BackpropTrainer(net, dataset, learningrate = 0.01, momentum = 0, verbose = False)
		t.trainEpochs(epochs=1)

		print("Finished Training: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
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
