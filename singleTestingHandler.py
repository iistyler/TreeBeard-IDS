from databaseObject import *
from nntrainer import *
from nnbuilder import *
import os
import xml.etree.ElementTree
import numpy as np
import time
import testingHandler



class SingleTestingHandler(testingHandler.testingHandler):
    """
        This class is just an extension of the testingHandler, however instead of 
        testing all the connections from the database at once, it will test individual
        connections. This allows for more precise control over timing exactly how 
        long each connection will take.
    """

    def testWholeNetwork(self):
        """
            This function overrides the testingHandler's function and implements 
            a different way to test the network. 
        """

        # Get the fields that the whole network uses
        fields = self.getNeededFields(self.netDict)
        neededInputFields = fields[0]
        neededSuccessFields = fields[1]

        # Save the attack list
        self.attackList = neededSuccessFields

        # Get the needed data 
        data = self.fetchData(neededInputFields, neededSuccessFields, [1])
        
        # Loop through each connection and test it 
        for i in data:
            self.testNetworkOnConn(self.netDict, i)

    
    def testNetworkOnConn(self, netDict, connection):
        """
            This function is used to test a single connection through the network
            and log what happens when testing it. Logging the following info:

            Conn Type, Net Predicted Conn Type, Time Through Net, Levels Traversed
            Output Values of Net At each level
        """
        
        self.testSingleNet(netDict["normal"], connection)



    def testSingleNet(self, currentNet, connection):
         
        # Get needed data
        data_list = self.extractData(currentNet.input, currentNet.success, connection)
        nn = currentNet.nn

        # Start the timer
        start_time = time.time()
        result = nn.activate(data_list[0])[0]
        end_time = time.time()
        total_time = end_time - start_time

        # Get the type of the connection
        conn_type = self.getConnType(connection)
    
        print "Time: " + str(total_time)
        print "Net Checked for: " + currentNet.success
        print "Connection was of type: " + conn_type
        print "NN resulted in value: " + str(result)
        

    
    def extractData(self, input_list, success, connection):
        """
            This function extracts the needed data from the connection based on 
            what the network needs for input and output. Returns a tuple that 
            holds the list of the input value and the success value
        """
        input_value_list = []

        for k, v in connection.iteritems():
            
            # If the key matches, put its value in the list
            if k in input_list:
                input_value_list.append(v)
            
            if k == success:
                success_val = v

        return (input_value_list, v)


    def fetchData(self, fields, success, ids):
        """
            This function overrides the testingHandler's function and implements 
            a different way to get data. We need this to ensure the data is in a 
            format so that each individual network has access to their own input 
            fields.
        """
        db = Database()

        fields = fields + success
        fields.append("id")
        
        data = db.getFields(fields, "test", ids)
        return data

    
    def getNeededFields(self, netDict):
        
        input_list = []
        success_list = []

        for k, v in netDict.iteritems():

            # Collect all the new features and add to main list
            in_old = set(input_list)
            in_new = set(v.input)
            new_items = in_new - in_old
            input_list = input_list + list(new_items)
            
            # Add the success criteria to the list, all net's have distinct 
            # success criteria.
            success_list.append(v.success)

        return (input_list, success_list)


    def getConnType(self, connection):
        """
            This function extracts the connection type by finding the dict value that 
            corresponds to an attack, and has the value of 1.
        """
        for k, v in connection.iteritems():
            if k in self.attackList and v == 1:
                return k


if __name__ == '__main__':

    test = SingleTestingHandler("exampleSchema")
    test.testWholeNetwork()
