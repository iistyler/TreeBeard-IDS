from databaseObject import *
import xml.etree.ElementTree

class testingHandler:
    def __init__(self):
        print("Created")

    def openSchema(self, fileName):

        # Setup dictionaries for XML
        networkDict = {}
        thresholdDict = {}

        # Parse xml file
        xmlHead = xml.etree.ElementTree.parse("XMLSchema/" + fileName + ".xml").getroot()

        # add details to dicts
        self.addAllDict(networkDict, thresholdDict, xmlHead.get('name'), xmlHead)
        print(networkDict["dos"])

    def addAllDict(self, networkDict, thresholdDict, lastName, lastNet):

        # Add each node info into dict
        for xmlNode in lastNet.findall('network'):
            netName = xmlNode.get('name')

            # Go to next node within
            self.addAllDict(networkDict, thresholdDict, netName, xmlNode)

            # Add to dict
            networkDict.setdefault(lastName, [])
            thresholdDict[netName] = xmlNode.get('threshold')
            networkDict[lastName].append( netName )

# TEST
testingH1 = testingHandler()
testingH1.openSchema("exampleSchema");