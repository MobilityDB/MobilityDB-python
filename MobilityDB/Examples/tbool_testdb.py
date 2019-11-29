from MobilityDB import *

connectionObject = None

try:
	# Set the connection parameters to PostgreSQL
	connectionObject = psycopg2.connect(host='127.0.0.1', database='regtests', user='mobilitydb', password='')
	connectionObject.autocommit = True

	# Register MobilityDB data types
	MobilityDBRegister(connectionObject)

	cursor = connectionObject.cursor()

	# TBoolInst

	postgreSQL_select_Query = "select * from tbl_tboolinst order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tboolinst table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tboolinst =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	# TBoolI

	postgreSQL_select_Query = "select * from tbl_tbooli order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tbooli table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tbooli =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	# TBoolSeq

	postgreSQL_select_Query = "select * from tbl_tboolseq order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tboolseq table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tboolseq =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	# TBoolS

	postgreSQL_select_Query = "select * from tbl_tbools order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tbools table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tbools =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

except psycopg2.DatabaseError as e:

	print('Error {e}')

finally:

	if connectionObject:
		connectionObject.close()
