from databaseObject import *
from nntrainer import *
from nnbuilder import *
import os
import xml.etree.ElementTree
import time
import Queue
import multiprocessing
import numpy as np

THREADS = 2

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
        newArr = db.getFields(fields, "test", ids)
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

    def testNetInner(self, x, return_dict, net, threshold, fields, successField, ids):
        correct = 0
        total = 0
        correctOfType = 0
        totalOfType = 0
        falsePositives = 0
        sendLower = []

        # Fetch data from DB
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

        returnData = [correct, total, correctOfType, totalOfType, falsePositives, sendLower]
        return_dict[x] = returnData

    def testNet(self, net, threshold, fields, successField, ids):
        correct = 0
        total = 0
        correctOfType = 0
        totalOfType = 0
        falsePositives = 0
        sendLower = []
        x = 0
        threshold = float(threshold)
        db = Database();

        # Fetch ids for splitting
        if (ids == None):
            ids = db.getAllIds()

        idsSet = np.array_split(ids, THREADS)

        start = time.time()

        # Setup return data from threads
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        processes = []

        # Create thread for each set of work
        for idsInnerSet in idsSet:
            x += 1
            # Delegate work to new process
            thread = multiprocessing.Process(target = self.testNetInner , args = (x, return_dict, net, threshold, fields, successField, idsInnerSet))
            thread.start()
            processes.append(thread)

        # Wait for processes to finish
        for i in range(THREADS):
            processes[i].join()

        # Add back all the return data
        for threadReturnData in return_dict.values():
            correct += threadReturnData[0]
            total += threadReturnData[1]
            correctOfType += threadReturnData[2]
            totalOfType += threadReturnData[3]
            falsePositives += threadReturnData[4]
            sendLower += threadReturnData[5]

        end = time.time()

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

        # Print results
        print("Correct: " + str(correct) + ", incorrect: " + str(total-correct) + ", of a total of: " + str(total))
        print("Correctly detrmined " + str(percent) + "% of connections")
        print("With " + str(totalOfType) + " of type " + successField + ", found " + str(correctOfType) + " of the " + str(totalOfType) + " which is " + str(percentOfTotal) + "%")
        print("Got " + str(falsePositives) + " false positives")
        print("Possible threats found: " + str( len(sendLower) ))
        print("Took " + str(end - start) + " seconds")

        # Returns percent correctly determined
        return sendLower;
