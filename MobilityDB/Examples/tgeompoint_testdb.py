from MobilityDB import *

connectionObject = None

try:
	# Set the connection parameters to PostgreSQL
	connectionObject = psycopg2.connect(host='127.0.0.1', database='regtests', user='mobilitydb', password='')
	connectionObject.autocommit = True

	# Register MobilityDB data types
	MobilityDBRegister(connectionObject)

	cursor = connectionObject.cursor()

	# TGeomPointInst

	postgreSQL_select_Query = "select * from tbl_tgeompointinst order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tgeompointinst table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tgeompointinst =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	# TGeomPointI

	postgreSQL_select_Query = "select * from tbl_tgeompointi order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tgeompointi table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tgeompointi =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	# TGeomPointSeq

	postgreSQL_select_Query = "select * from tbl_tgeompointseq order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tgeompointseq table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tgeompointseq =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	# TGeomPointS

	postgreSQL_select_Query = "select * from tbl_tgeompoints order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tgeompoints table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tgeompoints =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

except psycopg2.DatabaseError as e:

	print('Error {e}')

finally:

	if connectionObject:
		connectionObject.close()
