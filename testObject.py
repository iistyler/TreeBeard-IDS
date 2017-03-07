from nnbuilder import *
from databaseObject import *
from nntrainer import *
from testingHandler import *

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

#-------------

# TEST
# testingH1 = testingHandler()
# testingH1.openSchema("exampleSchema");

#----------------------------

# newTrainer = NNTrainer()

# test = NNBuilder("exampleNetwork")
# nn = test.BuildNN()

# # Create dataset
# testDataset = newTrainer.createDataset(test.input, test.success)
# print("Created test dataset")

# # Train network
# t = newTrainer.trainNetwork(nn, testDataset)
# print("Trained network")

# # Crete testing framework
# testHandler = testingHandler();

# testHandler.testNet(nn, 0.5, test.input, test.success)


#----------------------------

testHandler = testingHandler("smallSchema");

print("\nTest Normal")
netBuilt = testHandler.netDict["normal"];
testHandler.testNet(netBuilt.nn, 0.5, netBuilt.input, netBuilt.success)


print("\nTest Probe")
netBuilt = testHandler.netDict["probe"];
testHandler.testNet(netBuilt.nn, 0.5, netBuilt.input, netBuilt.success)






