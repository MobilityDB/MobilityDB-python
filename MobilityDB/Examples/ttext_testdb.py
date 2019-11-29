from MobilityDB import *

connectionObject = None

try:
	# Set the connection parameters to PostgreSQL
	connectionObject = psycopg2.connect(host='127.0.0.1', database='regtests', user='mobilitydb', password='')
	connectionObject.autocommit = True

	# Register MobilityDB data types
	MobilityDBRegister(connectionObject)

	cursor = connectionObject.cursor()

	# TTextInst

	postgreSQL_select_Query = "select * from tbl_ttextinst order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_ttextinst table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("ttextinst =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	# TTextI

	postgreSQL_select_Query = "select * from tbl_ttexti order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_ttexti table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("ttexti =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	# TTextSeq

	postgreSQL_select_Query = "select * from tbl_ttextseq order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_ttextseq table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("ttextseq =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	# TTextS

	postgreSQL_select_Query = "select * from tbl_ttexts order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_ttexts table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("ttexts =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

except psycopg2.DatabaseError as e:

	print('Error {e}')

finally:

	if connectionObject:
		connectionObject.close()
