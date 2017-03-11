#!/usr/bin/python
import MySQLdb

testOnly = 1

class Database:

	def __init__(self):

		self.db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  		  # your password
                     db="KDD")            # name of the data base

	# Get all IDs in table
	def getAllIds(self):
		cur = self.db.cursor(MySQLdb.cursors.DictCursor)
		table = "allData2"

		# override if you dont want to use the full database
		if (testOnly == 1):
			table = "testData"

		# Query for all IDs
		cur.execute("SELECT id FROM " + table)
		result_set = cur.fetchall()
		self.db.commit()
		returnData = []

		# Put all ids into array
		for row in result_set:
			returnData.append(row['id'])

		return returnData


	def getFields(self, fields, tableType, ids):
		cur = self.db.cursor(MySQLdb.cursors.DictCursor)
		addString = ""

		# Should not import any data
		if (ids != None and len(ids) <= 0):
			addString = " WHERE 1=2 "

		# Add all IDs
		elif (ids != None ):
			addString = " WHERE id IN (" + str(ids[0])
			for identifier in ids[1:]:
				addString += " , " + str(identifier)
			addString += ") "

		# Add each field
		fieldList = fields[0]
		for field in fields[1:]:
			fieldList += ","
			fieldList += field

		# Check type of data and override to avoid full database
		if (tableType == "test" or testOnly == 1):
			table = "NBTrain"
		else:
			table = "NBTest"

		# Use all the SQL you like
		cur.execute("SELECT " + fieldList + " FROM " + table + addString) #ORDER BY RAND()

		result_set = cur.fetchall()
		self.db.commit()

		return result_set