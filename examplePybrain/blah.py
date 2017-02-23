from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised import BackpropTrainer
from pybrain.structure import *
import struct


def make_dataset():
    """
    Creates a set of training data.
    """
    data = SupervisedDataSet(2,1)

    data.addSample([1,1],[0])
    data.addSample([1,0],[1])
    data.addSample([0,1],[1])
    data.addSample([0,0],[0])

    return data


def training(d, n):
    """
    Builds a network and trains it.
    """
    
    t = BackpropTrainer(n, d, learningrate = 0.01, momentum = 0.99, verbose = False)
    for epoch in range(0,100):
        t.train()

    return t


def test(trained):
    """
    Builds a new test dataset and tests the trained network on it.
    """
    testdata = SupervisedDataSet(2,1)
    testdata.addSample([1,1],[0])
    testdata.addSample([1,0],[1])
    testdata.addSample([0,1],[1])
    testdata.addSample([0,0],[0])
    averageError = trained.testOnData(testdata, verbose= False)
    return averageError

def deconstructNetwork():
	print("a")

def constructNetwork(n):
	n.addInputModule(inLayer)
	n.addModule(hiddenLayer)
	n.addOutputModule(outLayer)
	print("b")

def binary(num):
    return ''.join(bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', num))

# def as_float32(self):
#     """
#     See: http://en.wikipedia.org/wiki/IEEE_754-2008
#     """
    
#     s = self.bitlist
#     return unpack("f",pack("I", bits2int(s)))

# # Where the bits2int function converts bits to an integer.  
# def bits2int(bits):
#     # You may want to change ::-1 if depending on which bit is assumed
#     # to be most significant. 
#     bits = [int(x) for x in bits[::-1]]

#     x = 0
#     for i in range(len(bits)):
#         x += bits[i]*2**i
#     return x

def pesos_conexiones(n, n2):
	string = "";

	for mod in n.modules:
		for conn in n.connections[mod]:
			string += " ";
			n.connections[conn] = 1;
			# print conn
			for cc in range(len(conn.params)):
				string += str(conn.whichBuffers(cc))
				string += str(conn.params[cc])
				# print conn.whichBuffers(cc), conn.params[cc]

	print("\n\n")
	print(string)

	# binB= struct.unpack('d', struct.pack('Q', int(s2, 0)))[0]
	# f = int(binR, 2)
	# print(struct.unpack('f', struct.pack('I', f))[0])

def checkError(n, trained):
	# do avg error checking
    error = 0;
    for runs in range(0, 20):
    	error += test(trained)
    error /= 20

    return error

def run():
    """
    Use this function to run build, train, and test your neural network.
    """
    trainingdata = make_dataset()

    n = buildNetwork(trainingdata.indim, 4, trainingdata.outdim,recurrent=True)
    trained = training(trainingdata, n)

    n2 = buildNetwork(trainingdata.indim, 4, trainingdata.outdim,recurrent=True)
    trained2 = training(trainingdata, n2)


    first = checkError(n, trained)
    second = checkError(n2, trained2)

    pesos_conexiones(n, n2)
    trained3 = training(trainingdata, n)

    third = checkError(n, trained)

    print(first,"-",second,"-",third)

    return 1
