'''
    Information to collect from the csv file:

    -> Total number of connections
    -> Total Normal Connections
    -> Total Malicious Connections
    -> Correctly Classified Connections (normal = normal, malicious = malicious)
    -> Incorrectly Classified Connections
    -> Correctly Identified Attacks
    -> Normal connections marked as malicious
    -> Malicious connections marked as normal
    -> Connections traversed down each layer
    -> Total run time
    -> Average run time
    -> Average run time per layer
'''

import csv
import sys

def common_elements(list1, list2):
    return list(set(list1) & set(list2))

# Information to track
correct = 0
incorrect = 0
false_normal_conn = 0
false_malic_conn = 0
one_layer = 0
two_layer = 0
three_layer = 0
total_time = 0.0

# Keep track of total times for each layer, and each datapoint for R analysis
layer_times = [ 0.0 , 0.0, 0.0 ]
layer_times_list = [ [], [], [] ]

# Total number of connections 
normal_conn = 0
malicious_conn = 0

# Number of connections classified as wrong attack type
wrong_conn_type = 0

f = open(sys.argv[1], 'rt')

try:
    reader = csv.reader(f)
    
    for row in reader:

        time = float(row[2])
        total_time += time

        connection_type = eval('[' + row[0].replace("*", ",") + ']')[0]
        predicted_conn_type = eval('[' + row[1].replace("*", ",") + ']')[0]
        
        # Check what type the connection was 
        if "normal" in connection_type:
            normal_conn += 1
        else:
            malicious_conn += 1

        if len(common_elements(connection_type, predicted_conn_type)) > 0:
            correct += 1
        else:
            
            # If it was classified as wrong attack type 
            if "normal" not in connection_type and "normal" not in predicted_conn_type:
                wrong_conn_type += 1
            else: 
                incorrect += 1

            # Predicted Normal
            if "normal" in predicted_conn_type:
                false_normal_conn += 1
            else:
                false_malic_conn += 1

        if row[3] == '3':
            three_layer += 1
            layer_times[2] += time
            layer_times_list[2].append(time)
        elif row[3] == '2':
            two_layer += 1
            layer_times[1] += time
            layer_times_list[1].append(time)
        else:
            one_layer += 1
            layer_times[0] += time
            layer_times_list[0].append(time)


finally:
    f.close()


total = normal_conn + malicious_conn

# This assertion should never fail or something went horribly wrong
assert total == correct + incorrect + wrong_conn_type

print "Total: " + str(total)
print "Normal: " + str(normal_conn)
print "Malicious: " + str(malicious_conn)
print "Correct: " + str(correct) + "(" + str(correct / float(total)) + ")"
print "Incorrect: " + str(incorrect) + "(" + str(incorrect / float(total)) + ")"
print "Correctly Identified Malicious Connections: " + str(malicious_conn - false_normal_conn - wrong_conn_type)
print "Marked as Malicious but Normal: " + str(false_malic_conn)
print "Marked as Normal but is Malicious: " + str(false_normal_conn)
print "Classified as Wrong attack type: " + str(wrong_conn_type)
print "Traversed down 1 layer: " + str(one_layer)
print "Traversed down 2 layers: " + str(two_layer)
print "Traversed down 3 layers: " + str(three_layer)
print "Total time: " + str(total_time)
print "Average time: " + str(total_time / float(total))
print "Layer 1 Average Time: " + '{0:f}'.format(layer_times[0] / float(one_layer))
print "Layer 2 Average Time: " + str( layer_times[1] / float(two_layer))
print "Layer 3 Average Time: " + str( layer_times[2] / float(three_layer))


# Some defined flags to dump R readable information
if len(sys.argv) > 2:
    flag = sys.argv[2]
else:
    flag = ""

if flag == "-t":
    print "Dumping time information"

    f = open("times.csv", "w")
    f.write("Layer,Time\n")
    
    lnum = 0
    for layer in layer_times_list:
        lnum += 1
        for time in layer:
            f.write(str(lnum) + "," + '{0:f}'.format(time) + "\n")
    f.close()
