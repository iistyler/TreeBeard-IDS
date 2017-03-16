#!/usr/bin/python
import MySQLdb
import sys

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  		  # your password
                     db="KDD")            # name of the data base

attackType = sys.argv[1]
		
cur = db.cursor(MySQLdb.cursors.DictCursor)

types = ["duration", "src_bytes", "dst_bytes", "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate"]
compare = []

print("Finding correlations to " + attackType)

for curType in types:
	for x in range(2):
		direction = ""
		if (x == 1):
			direction = "!"

		cur.execute("SELECT SUM("+curType+") AS total, count("+curType+") AS num FROM NBTrain WHERE " + attackType + " " + direction + "= 1")
		result_set = cur.fetchall()

		# Put all ids into array
		total = float(result_set[0]['total'])
		num = float(result_set[0]['num'])

		if (x == 1):
			avg1 = total / num
		else:
			avg2 = total / num

	#Skip 
	if (avg1 == 0 or avg2 == 0):
		continue;
		
	# Find 2 averages
	if (avg1 > avg2):
		if (avg2 != 0):
			diff = avg1 / avg2
		else:
			diff = 0
	else:
		if (avg1 != 0):
			diff = avg2 / avg1
		else:
			diff = 0

	compare.append([curType, diff])


compare.sort(key=lambda x: x[1])
compare.reverse()

for cur in compare:
	print(cur)