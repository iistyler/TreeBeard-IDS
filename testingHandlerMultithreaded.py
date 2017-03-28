from databaseObject import *
from nntrainer import *
from nnbuilder import *
import os
import xml.etree.ElementTree
import time
import Queue
import multiprocessing
import numpy as np

THREADS = 3

NEWONLY = 0

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

        if (netExists and NEWONLY != 1):
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
            
            testDataset = netTrainer.createDataset(builder.input, builder.success, builder.typeRuns, builder.normRuns)

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
        newArr = db.getFields(fields, "test", ids, None)
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
        normalAsThreat = 0
        sendLower = []

        # Fetch data from DB
        checkData = self.fetchData(fields, successField, ids)
        blah = 0
        blah2 = 0

        # Test each record
        for row in checkData:
            result = net.activate(row[0])[0]
            expected = row[1]
            totalOfType += expected

            # Guess is whether not it is believed to be malicious
            if result >= threshold:
                guess = 1
            else:
                guess = 0

            # Flip normals
            if successField == "normal":
                if guess == 0:
                    sendGuess = 1
                elif guess == 1:
                    sendGuess = 0
            else:
                sendGuess = guess

            # Net believes malicious
            if sendGuess == 1:
                sendLower.append(row[2])

            # net believes malicious and is
            if guess == 1 and expected == 1:
                correct += 1.0
                correctOfType += 1.0

            # net believes not malicious and isnt
            if guess == 0 and expected == 0:
                correct += 1.0

            # net belivies malicious but is not
            if guess == 1 and expected == 0:
                normalAsThreat += 1.0

            # net believes not malicious but is
            if guess == 0 and expected == 1:
                falsePositives += 1.0

            # Normal has reversed stats
            if successField == "normal":
                tempFalse = falsePositives
                falsePositives = normalAsThreat
                normalAsThreat = tempFalse

            total += 1.0            # To prevent integer division

        returnData = [correct, total, correctOfType, totalOfType, falsePositives, sendLower, normalAsThreat]
        return_dict[x] = returnData

    def testNet(self, net, threshold, fields, successField, ids):
        correct = 0
        total = 0
        correctOfType = 0
        totalOfType = 0
        falsePositives = 0
        normalAsThreat = 0
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
            normalAsThreat += threadReturnData[6]

        end = time.time()

        # Calculate percent correctly determined
        if (total > 0):
            percent = correct/total
        else:
            percent = 1
        percent *= 100.0

        # Total of type
        percentOfTotal = 0
        if (totalOfType != 0):
            percentOfTotal = correctOfType/totalOfType*100
        else:
            percentOfTotal = 100

        quality = (percent + percentOfTotal) / 2

        # Print results
	print("Threshold: " + str(threshold));
        print("Correct: " + str(correct) + ", incorrect: " + str(total-correct) + ", of a total of: " + str(total))
	print("Correctly determined " + str(percent) + "% of connections")
        print("With " + str(totalOfType) + " of type " + successField + ", found " + str(correctOfType) + " of the " + str(totalOfType) + " which is " + str(percentOfTotal) + "%")
        print("Number of threats classified as normal: " + str(falsePositives))
        print("Number of normals classified as threats: " + str(normalAsThreat))
        print("Possible threats found: " + str( len(sendLower) ))
        print("Took " + str(end - start) + " seconds")
        print("Quality of net " + str(int(quality)) + "%")

        # Returns percent correctly determined
        return sendLower;
