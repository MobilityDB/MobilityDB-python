from MobilityDB import *

connectionObject = None

try:
	# Set the connection parameters to PostgreSQL
	connectionObject = psycopg2.connect(host='127.0.0.1', database='regtests', user='mobilitydb', password='')
	connectionObject.autocommit = True

	# Register MobilityDB data types
	MobilityDBRegister(connectionObject)

	cursor = connectionObject.cursor()

	# TGeogPointInst

	postgreSQL_select_Query = "select * from tbl_tgeogpointinst order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tgeogpointinst table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tgeogpointinst =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	# TGeogPointI

	postgreSQL_select_Query = "select * from tbl_tgeogpointi order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tgeogpointi table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tgeogpointi =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	# TGeogPointSeq

	postgreSQL_select_Query = "select * from tbl_tgeogpointseq order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tgeogpointseq table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tgeogpointseq =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	# TGeogPointS

	postgreSQL_select_Query = "select * from tbl_tgeogpoints order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tgeogpoints table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tgeogpoints =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

except psycopg2.DatabaseError as e:

	print('Error {e}')

finally:

	if connectionObject:
		connectionObject.close()
