from nnobject import *
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

newTrainer = NNTrainer();

test = NNBuilder("exampleNetwork")
nn = test.BuildNN()

# fields = ["duration", "tcp", "dst_bytes", "normal"]
newDataset = newTrainer.createDataset(test.input, test.success, "test")

t = newTrainer.trainNetwork(10, nn, newDataset)

t.testOnData(newDataset, verbose= True)

# print newDataset