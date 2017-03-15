import json
import sys
import pprint
import os

from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection, BiasUnit

class NNBuilder:

        # Don't see why we would change this but just incase
        OUTPUT_NODES = 1

        def __init__(self, file):
            netExists = os.path.isfile('JSONNetDesc/' + file)

            if (netExists == False):
                print("No net description exists for " + file)
                sys.exit()

            with open('JSONNetDesc/' + file) as data_file:    
                data = json.load(data_file)
            
            self.name = file
            self.hiddenLayers = data["hiddenLayers"]
            self.success = data["success"]
            self.input = data["input"]
            self.typeRuns = data["typeRuns"]
            self.normRuns = data["normRuns"]
            self.nn = None
                
        
        def getName(self):
            return self.name

        def getHiddenLayers(self):
            return self.hiddenLayers

        def getInput(self):
            return self.input

        def BuildNN(self):
            """ 
                This function builds a FeedForwardNetwork object based on 
                the data that was used to create the NNBuilder object
            """
            nn = FeedForwardNetwork()

            # Set up the Layers
            inputLayer = LinearLayer(len(self.getInput()))
            outputLayer = SigmoidLayer(self.OUTPUT_NODES)
            
            # Add to NN
            nn.addInputModule(inputLayer)
            nn.addOutputModule(outputLayer)

            # Handle multiple hidden layers, add to NN
            topology = self.getHiddenLayers()
            hiddenLayers = []

            for i in range(0, len(topology)):
                size = int(topology[i])
                hlayer = SigmoidLayer(size)
                nn.addModule(hlayer)
                hiddenLayers.append(hlayer)

            # Get the bias for each hidden layer
            biasList = []
            for i in range(0, len(topology)):
                bias = BiasUnit(name = "bias" + str(i))
                nn.addModule(bias)
                biasList.append(bias)

            # Manually connect input layer to first hidden, 
            # and output layer to last hidden. Then connect all other
            # hidden layers
            input2hidden = FullConnection(inputLayer, hiddenLayers[0])
            hidden2output = FullConnection(hiddenLayers[-1], outputLayer)

            # If there was more than 1 hidden layer connect them together
            hiddenConList = []
            biasConList = []
            if len(topology) > 1:
                for i in range(0, len(topology) - 1):
                    
                    # Connect current layer to next layer
                    connection = FullConnection(hiddenLayers[i], hiddenLayers[i + 1])
                    hiddenConList.append(connection)

                    # Make connection for bias 
                    biasConList.append(FullConnection(biasList[i], hiddenLayers[i]))
            
            # Since we only looped to  < len(topology) - 1, have to get the last layer
            last = len(topology) - 1
            biasConList.append(FullConnection(biasList[last], hiddenLayers[last]))

            # Add connections to the NN
            nn.addConnection(input2hidden)
            for i in hiddenConList:
                nn.addConnection(i)
            for i in biasConList:
                nn.addConnection(i)
            nn.addConnection(hidden2output)

            # Not sure what this does but need to call it 
            nn.sortModules()

            self.nn = nn
            return nn




""" Testing functionality of object """
if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)

    if len(sys.argv) < 2:
        print "To test output data run: python nnbuilder.py [json file name]"
        sys.exit()

    test = NNBuilder(sys.argv[1])
    
    print("NNBuilder has the data: ")
    pp.pprint(test.getName())
    pp.pprint(test.getHiddenLayers())
    pp.pprint(test.getInput())

    nn = test.BuildNN()

    print("\nPrinting NN Structure:")
    print nn

