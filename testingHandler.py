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
        self.head = topLayer
        self.netDict[ topLayer ] = self.fetchNet( topLayer )
        self.thresholdDict[ topLayer ] = xmlHead.get('threshold')

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

    def fetchData(self, fields, successField, ids):
        db = Database();

        fields.append(successField)
        fields.append("id")
        newArr = db.getFields(fields, "all", ids)
        returnArr = []

        # Get each row from DB
        for row in newArr:
            arr = []

            # Append each field to dataset
            for field in fields:
                if (field != successField and field != "id"):
                    arr.append(row[field]);

            # Add sample to set
            returnArr.append([arr, row[successField], row["id"]])

        # Remve the success field
        fields.pop()
        fields.pop()

        return returnArr;

    def testWholeNetwork(self):
        self.testEach(self.head, None)

    def testEach(self, name, arr):
        netBuilt = self.netDict[name]
        threshold = self.thresholdDict[name]

        print("\nTesting " + name + " with a success at " + netBuilt.success)
        arr = self.testNet(netBuilt.nn, threshold, netBuilt.input, netBuilt.success, arr)

        if name in self.networkDescDict.keys():

            netNames = self.networkDescDict[name]
            for netName in netNames:
                self.testEach(netName, arr)

    def testNet(self, net, threshold, fields, successField, ids):
        correct = 0
        total = 0
        correctOfType = 0
        totalOfType = 0
        falsePositives = 0
        sendLower = []
        threshold = float(threshold)

        checkData = self.fetchData(fields, successField, ids)

        # Test each record
        for row in checkData:
            result = net.activate(row[0])[0]
            expected = row[1];
            totalOfType += expected;

            # Check if within threshold - correctly identified what looking for
            if (expected == 1 and result > threshold):
                correct += 1.0      # To prevent integer division
                correctOfType += 1.0

                if (successField != "normal"):
                    sendLower.append(row[2])

            if (expected == 0 and result < threshold):
                correct += 1.0

                if (successField == "normal"):
                    sendLower.append(row[2])

            # Check if false positive
            if (expected == 0 and result > threshold and successField == "normal"):
                falsePositives += 1.0

            if (expected == 1 and result < threshold and successField != "normal"):
                falsePositives += 1.0

            total += 1.0            # To prevent integer division

        # Calculate percent correctly determined
        if (total > 0):
            percent = correct/total
        else:
            percent = 0
        percent *= 100.0

        # Total of type
        percentOfTotal = 0
        if (totalOfType != 0):
            percentOfTotal = correctOfType/totalOfType*100

        print("Correct: " + str(correct) + ", incorrect: " + str(total-correct) + ", of a total of: " + str(total))
        print("Correctly detrmined " + str(percent) + "% of connections")
        print("With " + str(totalOfType) + " of type " + successField + ", found " + str(correctOfType) + " of the " + str(totalOfType) + " which is " + str(percentOfTotal) + "%")
        print("Got " + str(falsePositives) + " false positives")
        print("Possible threats found: " + str( len(sendLower) ))

        # Returns percent correctly determined
        return sendLower;


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print "Usage: python testingHandler.py [xml schema]"
        sys.exit()

    testHandler = testingHandler("justNormal")
    testHandler.testWholeNetwork()
