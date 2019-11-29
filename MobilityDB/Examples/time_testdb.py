from MobilityDB import *

connectionObject = None

try:
	# Set the connection parameters to PostgreSQL
	connectionObject = psycopg2.connect(host='127.0.0.1', database='regtests', user='mobilitydb', password='')
	connectionObject.autocommit = True

	# Register MobilityDB data types
	MobilityDBRegister(connectionObject)

	cursor = connectionObject.cursor()

	# TimestampSet

	postgreSQL_select_Query = "select * from tbl_timestampset order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_timestampset table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("timestampset =", row[1])
		if not row[1]:
			print("")
		else:
			print("timespan =", row[1].timespan(), "\n")

	# Period

	postgreSQL_select_Query = "select * from tbl_period order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_period table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("period =", row[1])
		if not row[1]:
			print("")
		else:
			print("timespan =", row[1].timespan(), "\n")

	# PeriodSet

	postgreSQL_select_Query = "select * from tbl_periodset order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_periodset table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("periodset =", row[1])
		if not row[1]:
			print("")
		else:
			print("timespan =", row[1].timespan(), "\n")

except psycopg2.DatabaseError as e:

	print('Error {e}')

finally:

	if connectionObject:
		connectionObject.close()
