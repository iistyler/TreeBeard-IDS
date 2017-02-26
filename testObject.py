from nnobject import *
from databaseObject import *

# net = NNObject("exampleNetwork");

# print ( net.name )

# for current in net.input:
# 	print ( current )

#------------------------------
db = Database();

fields = ["id", "dst_bytes"]
newArr = db.getFields(fields, "test")

for row in newArr:
	print(row["dst_bytes"])