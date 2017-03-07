from databaseObject import *
from nntrainer import *
from nnbuilder import *
import os
import xml.etree.ElementTree

class testingHandler:
    def __init__(self, fileName):
        self.openSchema(fileName)

    def openSchema(self, fileName):

        # Setup dictionaries for XML
        self.networkDescDict = {}
        self.netDict = {}
        self.thresholdDict = {}

        # Parse xml file
        xmlHead = xml.etree.ElementTree.parse("XMLSchema/" + fileName + ".xml").getroot()
        topLayer = xmlHead.get('name')
        self.netDict[ topLayer ] = self.fetchNet( topLayer )

        # add details to dicts
        self.addAllDict(self.networkDescDict, self.thresholdDict, self.netDict, xmlHead.get('name'), xmlHead)

    def addAllDict(self, networkDescDict, thresholdDict, netDict, lastName, lastNet):

        # Add each node info into dict
        for xmlNode in lastNet.findall('network'):
            netName = xmlNode.get('name')

            # Go to next node within
            self.addAllDict(networkDescDict, thresholdDict, netDict, netName, xmlNode)

            # Add to dict
            networkDescDict.setdefault(lastName, [])
            thresholdDict[netName] = xmlNode.get('threshold')
            networkDescDict[lastName].append( netName )
            netDict[netName] = self.fetchNet( netName )

    def fetchNet(self, name):
        fileName = "NetBinarySaves/" + name
        netExists = os.path.isfile(fileName)

        if (netExists):
            # See if net was already created
            print("Using existing net for " + name)
            importFile = open(fileName,'r')
            builder = pickle.load(importFile)
        else:
            # Create net if it doesnt already exist
            print("Creating net for " + name)
            builder = NNBuilder(name)
            builder.BuildNN()
            net = builder.nn

            netTrainer = NNTrainer()

            # Create the dataset
            print("Creating dataset for " + name)
            testDataset = netTrainer.createDataset(builder.input, builder.success)

            # Train the network
            print("Training " + name)
            netTrainer.trainNetwork(net, testDataset)

            # Save the built net
            print("Saving net")
            exportFile = open(fileName, 'w')
            pickle.dump(builder, exportFile)

        return builder

    def fetchData(self, fields, successField):
        db = Database();

        fields.append(successField)
        newArr = db.getFields(fields, "test")
        returnArr = []

        # Get each row from DB
        for row in newArr:
            arr = []

            # Append each field to dataset
            for field in fields:
                if (field != successField):
                    arr.append(row[field]);

            # Add sample to set
            returnArr.append([arr, row[successField]])

        # Remve the success field
        fields.pop()

        return returnArr;

    # def testWholeNetwork(self):


    def testNet(self, net, threshold, fields, successField):
        correct = 0
        total = 0;
        correctOfType = 0;
        totalOfType = 0;
        falsePositives = 0;

        checkData = self.fetchData(fields, successField)

        # Test each record
        for row in checkData:
            result = net.activate(row[0])[0]
            expected = row[1];
            totalOfType += expected;

            # Check if within threshold
            if (expected == 1 and result > threshold):
                correct += 1.0      # To prevent integer division
                correctOfType += 1.0

            # Check if under threshold
            if (expected == 0 and result < threshold):
                correct += 1.0

            # Check if false positive
            if (expected == 0 and result > threshold):
                falsePositives += 1.0

            total += 1.0            # To prevent integer division

        # Calculate percent correctly determined
        percent = correct/total
        percent *= 100.0

        # Total of type
        percentOfTotal = 0
        if (totalOfType != 0):
            percentOfTotal = correctOfType/totalOfType*100

        print("Correct: " + str(correct) + ", inorrect: " + str(total-correct))
        print("Correctly detrmined " + str(percent) + "% of connections")
        print("With " + str(totalOfType) + " of type " + successField + ", found " + str(correctOfType) + " of the " + str(totalOfType) + " which is " + str(percentOfTotal) + "%")
        print("Got " + str(falsePositives) + " false positives");

        # Returns percent correctly determined
        return percent;
