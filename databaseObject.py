#!/usr/bin/python
import MySQLdb

class Database:

	def __init__(self):

		self.db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  		  # your password
                     db="KDD")            # name of the data base

	def getFields(self, fields, tableType):
		cur = self.db.cursor(MySQLdb.cursors.DictCursor)

		fieldList = fields[0]
		for field in fields[1:]:
			fieldList += ","
			fieldList += field

		if (tableType == "test"):
			table = "testData"
		else:
			table = "allData"

		# Use all the SQL you like
		cur.execute("SELECT " + fieldList + " FROM " + table + " LIMIT 10000")

		result_set = cur.fetchall()
		self.db.commit()

		return result_set