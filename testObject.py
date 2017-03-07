from nnbuilder import *
from databaseObject import *
from nntrainer import *
from nnbuilder import *

# net = NNObject("exampleNetwork");

# print ( net.name )

# for current in net.input:
# 	print ( current )

#------------------------------
# db = Database();

# fields = ["id", "dst_bytes"]
# newArr = db.getFields(fields, "test")

# for row in newArr:
# 	print(row["dst_bytes"])

#----------------------------

newTrainer = NNTrainer()

test = NNBuilder("exampleNetwork")
nn = test.BuildNN()

testDataset = newTrainer.createDataset(test.input, test.success, "test")
print("Created test dataset")

t = newTrainer.trainNetwork(nn, testDataset)
print("Trained network")

allDataset = newTrainer.createDataset(test.input, test.success, "all")
print("Created all dataset")

# newTrainer.exportObj(allDataset, "temp/dataset")
# allDataset2 = newTrainer.importObj("temp/dataset")
# t2 = newTrainer.importObj("temp/t")

t2.testOnData(dataset=allDataset2, verbose= True)

# print newDataset