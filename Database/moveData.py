#!/usr/bin/python
import MySQLdb
import sys

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  		  # your password
                     db="KDD")            # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
# cur.execute("INSERT INTO testData (duration) VALUES (1) ")
cur.execute("TRUNCATE NBTest")
cur.execute("SELECT * FROM NBTestRaw")

# # print all the first cell of all the rows
for row in cur.fetchall():
	attackType = ""
	subAttackType = ""

	attackType = str(row[41]).strip('.');

	if (attackType == "land"):
		attackType = "a_land"

	if (attackType == "back" or attackType == "teardrop" or attackType == "pod" or attackType == "a_land" or attackType == "smurf" or attackType == "neptune" or attackType == "apache2" or attackType == "udpstrom" or attackType == "mailbomb" or attackType == "processtable" or attackType == "udpstorm"):
		subAttackType = "dos"
	elif (attackType == "ipsweep" or attackType == "nmap" or attackType == "portsweep" or attackType == "satan" or attackType == "saint" or attackType == "mscan"):
		subAttackType = "probe"
	elif (attackType == "rootkit" or attackType == "buffer_overflow" or attackType == "loadmodule" or attackType == "perl" or attackType == "ps" or attackType == "xterm" or attackType == "eject" or attackType == "sqlattack"):
		subAttackType = "u2r"
	elif (attackType == "multihop" or attackType == "ftp_write" or attackType == "guess_passwd" or attackType == "spy" or attackType == "imap" or attackType == "phf" or attackType == "warezclient" or attackType == "warezmaster" or attackType == "dictionary" or attackType == "named" or attackType == "sendmail" or attackType == "xlock" or attackType == "xsnoop" or attackType == "snmpgetattack" or attackType == "httptunnel" or attackType == "worm" or attackType == "snmpguess"):
		subAttackType = "r2l"
	elif (attackType == "normal"):
		subAttackType = "ignoreMe"
	else:
		print("Failed on " + attackType)
		sys.exit()


	statement = "INSERT INTO NBTest ("+attackType+", "+subAttackType+", "+row[1]+", "+row[2]+", "+row[3]+", duration, src_bytes, dst_bytes, land, wrong_fragment, urgent, hot, num_failed_logins, logged_in, num_compromised, root_shell, su_attempted, num_root, num_file_creations, num_shells, num_access_files, num_outbound_cmds, is_host_login, is_guest_login, count, srv_count, serror_rate, srv_serror_rate, rerror_rate, srv_rerror_rate, same_srv_rate, diff_srv_rate, srv_diff_host_rate, dst_host_count, dst_host_srv_count, dst_host_same_srv_rate, dst_host_diff_srv_rate, dst_host_same_src_port_rate, dst_host_srv_diff_host_rate, dst_host_serror_rate, dst_host_srv_serror_rate, dst_host_rerror_rate, dst_host_srv_rerror_rate, connection_type) VALUES (1, 1, 1, 1, 1, "+ str(row[0])+", "+ str(row[4])+", "+ str(row[5])+", "+ str(row[6])+", "+ str(row[7])+", "+ str(row[8])+", "+ str(row[9])+", "+ str(row[10])+", "+ str(row[11])+", "+ str(row[12])+", "+ str(row[13])+", "+ str(row[14])+", "+ str(row[15])+", "+ str(row[16])+", "+ str(row[17])+", "+ str(row[18])+", "+ str(row[19])+", "+ str(row[20])+", "+ str(row[21])+", "+ str(row[22])+", "+ str(row[23])+", "+ str(row[24])+", "+ str(row[25])+", "+ str(row[26])+", "+ str(row[27])+", "+ str(row[28])+", "+ str(row[29])+", "+ str(row[30])+", "+ str(row[31])+", "+ str(row[32])+", "+ str(row[33])+", "+ str(row[34])+", "+ str(row[35])+", "+ str(row[36])+", "+ str(row[37])+", "+ str(row[38])+", "+ str(row[39])+", "+ str(row[40])+", '"+ str(row[41]).strip('.')+"') "
	print(statement)
	cur.execute(statement)
	print (".")

db.commit()

db.close()
print ("Complete")