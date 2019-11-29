from MobilityDB import *

connectionObject = None

try:
	# Set the connection parameters to PostgreSQL
	connectionObject = psycopg2.connect(host='127.0.0.1', database='regtests', user='mobilitydb', password='')
	connectionObject.autocommit = True

	# Register MobilityDB data types
	MobilityDBRegister(connectionObject)

	cursor = connectionObject.cursor()

	# TIntInst

	postgreSQL_select_Query = "select * from tbl_tintinst order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tintinst table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tintinst =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	# TIntI

	postgreSQL_select_Query = "select * from tbl_tinti order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tinti table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tinti =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	# TIntSeq

	postgreSQL_select_Query = "select * from tbl_tintseq order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tintseq table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tintseq =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	# TIntS

	postgreSQL_select_Query = "select * from tbl_tints order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tints table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tints =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

except psycopg2.DatabaseError as e:

	print('Error {e}')

finally:

	if connectionObject:
		connectionObject.close()
