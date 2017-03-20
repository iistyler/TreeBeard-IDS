import csv
import sys

correct = 0
incorrect = 0
false_normal_conn = 0
false_malic_conn = 0
one_layer = 0
two_layer = 0
three_layer = 0
total_time = 0.0

f = open(sys.argv[1], 'rt')

try:
    reader = csv.reader(f)
    
    for row in reader:
        total_time += float(row[2])
        lastRow = eval('[' + row[0].replace("*", ",") + ']')[0]
        # print( str(lastRow) + " : " + row[1])

        if row[1] in lastRow:
            correct += 1
        else:
            incorrect += 1

            # Predicted Normal
            if row[1] == "normal":
                false_normal_conn += 1

            else:
                false_malic_conn += 1



        if row[3] == '3':
            three_layer += 1
        elif row[3] == '2':
            two_layer += 1
        else:
            one_layer += 1


finally:
    f.close()


total = correct + incorrect

print "Total: " + str(total)
print "Correct: " + str(correct) + "(" + str(correct / float(total)) + ")"
print "Incorrect: " + str(incorrect) + "(" + str(incorrect / float(total)) + ")"
print "Marked as Malicious but Normal: " + str(false_malic_conn)
print "Marked as Normal but is Malicious: " + str(false_normal_conn)
print "Traversed down 1 layer: " + str(one_layer)
print "Traversed down 2 layers: " + str(two_layer)
print "Traversed down 3 layers: " + str(three_layer)
print "Total time: " + str(total_time)
print "Average time: " + str(total_time / float(total))

