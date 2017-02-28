import json
import sys
import pprint

from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection

class NNBuilder:

        # Don't see why we would change this but just incase
        OUTPUT_NODES = 1

        def __init__(self, file):

            with open('JSONNetDesc/exampleNetwork') as data_file:    
                data = json.load(data_file)

            self.name = data["name"]
            self.hiddenLayers = data["hiddenLayers"]
            self.success = data["success"]
            self.input = data["input"]
                
        
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
            outputLayer = LinearLayer(self.OUTPUT_NODES)
            
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

            # Manually connect input layer to first hidden, 
            # and output layer to last hidden. Then connect all other
            # hidden layers
            input2hidden = FullConnection(inputLayer, hiddenLayers[0])
            hidden2output = FullConnection(hiddenLayers[-1], outputLayer)

            # If there was more than 1 hidden layer connect them together
            hiddenConList = []
            if len(topology) > 1:
                for i in range(0, len(topology) - 1):
                    connection = FullConnection(hiddenLayers[i], hiddenLayers[i + 1])
                    hiddenConList.append(connection)

            # Add connections to the NN
            nn.addConnection(input2hidden)
            for i in hiddenConList:
                nn.addConnection(i)
            nn.addConnection(hidden2output)

            # Not sure what this does but need to call it 
            nn.sortModules()

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
    print(nn)

