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
        data = self.fetchData(neededInputFields, neededSuccessFields, None)
        
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
        total_time = 0
        net_structure = self.networkDescDict
        current_net_list = [ "normal" ]
        layers_traversed = 0
        conn_type = self.getConnType(connection)
        predicted_conn_type = []


        #print "\n\nConnection is type: " + str(conn_type)

        # Loop through all layers
        for i in range(0, 3):
                
            #print "Layer " + str(i)
            subnets = []

            # If there are no subnets to check, that means a normal connection 
            # got through the first layer, and the lower nets think it's normal
            if len(current_net_list) == 0:
                break

            # If we don't need to check subnets
            done = 0
            

            # Loop through current nets in level. If they find something, add
            # their subnets to the next level to check.
            for net_name in current_net_list:

                #print "Testing net: " + net_name

                result = self.testSingleNet(netDict[net_name], connection)
                expected = result[1]
                time = result[2]

                # Add to running time
                total_time += time
            
                # Net has flagged the connection
                if result[0] == expected and expected == 1:

                    # If its the first layer we leave
                    if i == 0:
                        done = 1
                        break
                    # If it wasn't the last layer, move down    
                    elif i == 1:
                        subnets += net_structure[net_name]
                    else:
                        predicted_conn_type.append(net_name)    
            
                # If the first level has an output of 0, have to move on
                elif result[0] == expected and expected == 0 and i == 0:
                    subnets += net_structure[net_name]

                #if result != expected and i == 0:
                #    subnets += net_structure[net_name]

            layers_traversed += 1

            # Get the current layers name list
            current_net_list = subnets
            subnets = []

            # If we are done, don't check lower layers
            if done == 1:
                break
        
        if len(predicted_conn_type) == 0:
            predicted_conn_type.append("normal")

        #if len(predicted_conn_type) > 1:
        #    sys.stderr.write("Connection had more than 1 expected. Dumping info...")
        #    sys.stderr.write(connection)
        #    sys.stderr.write(predicted_conn_type)
        #print "Predicted: " + str(predicted_conn_type)

        print str(conn_type).replace(",", "*") + "," + predicted_conn_type[0] + "," + str(total_time) + "," + str(layers_traversed)


    def testSingleNet(self, currentNet, connection):
         
        # Get needed data
        data_list = self.extractData(currentNet.input, currentNet.success, connection)
        nn = currentNet.nn

        # Start the timer
        start_time = time.time()
        result = nn.activate(data_list[0])[0]
        end_time = time.time()
        total_time = end_time - start_time
        threshold = float(self.thresholdDict[currentNet.name])

        # Use the expected value to find out if this is the right output
        expected = data_list[1]
        
        #print "Net output: " + str(result) + "\t Expected: " + str(expected)
        
        # Normal connection so expected to be 1
        if result < threshold:
            return (0, expected, total_time, result)
        elif result >= threshold:
            return (1, expected, total_time, result)
        else:
            raise ValueError('Output from NN was not in range [0, 1]')

    
    def extractData(self, input_list, success, connection):
        """
            This function extracts the needed data from the connection based on 
            what the network needs for input and output. Returns a tuple that 
            holds the list of the input value and the success value
        """
        input_value_list = []
        success_val = 0

        for k, v in connection.iteritems():

            # If the key matches, put its value in the list
            if k in input_list:
                input_value_list.append(v)
            
            if k == success:
                success_val = v
        
        return (input_value_list, success_val)


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
        
        data = db.getFields(fields, "test", ids, None)
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

        #print success_list
        return (input_list, success_list)


    def getConnType(self, connection):
        """
            This function extracts the connection type by finding the dict value that 
            corresponds to an attack, and has the value of 1.
        """
        ctype = []
        for k, v in connection.iteritems():
            if k in self.attackList and v == 1:
                ctype.append(k)

        return ctype


if __name__ == '__main__':

    test = SingleTestingHandler("exampleSchema")
    test.testWholeNetwork()
