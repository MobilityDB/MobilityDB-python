from MobilityDB import *

connectionObject = None

try:
	# Set the connection parameters to PostgreSQL
	connection = psycopg2.connect(host='127.0.0.1', database='regtests', user='mobilitydb', password='')
	connection.autocommit = True

	# Register MobilityDB data types
	MobilityDBRegister(connection)

	cursor = connection.cursor()

	######################
	# TFloatInst
	######################

	drop_table_query = '''DROP TABLE IF EXISTS tbl_tfloatinst_temp;'''
	cursor.execute(drop_table_query)
	connection.commit()
	print("Table deleted successfully in PostgreSQL ")
	
	create_table_query = '''CREATE TABLE tbl_tfloatinst_temp
		(
		  k integer PRIMARY KEY,
		  temp tfloat
		); '''

	cursor.execute(create_table_query)
	connection.commit()
	print("Table created successfully in PostgreSQL ")

	postgreSQL_select_Query = "select * from tbl_tfloatinst order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tfloatinst table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tfloatinst =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	print(rows)
	print(type(rows[3]))

	rows1 = [(row[0],) for row in rows]
	print(rows1)
	print(type(rows1[3]))

	postgres_insert_query = ''' INSERT INTO tbl_tfloatinst_temp (k) VALUES (%s) '''
	result = cursor.executemany(postgres_insert_query, rows1)
	connection.commit()
	count = cursor.rowcount
	print(count, "record(s) inserted successfully into tbl_tfloatinst table")

	#postgres_insert_query = ''' INSERT INTO tbl_tfloatinst_temp (k, temp) VALUES (%s,%s) '''

	#record_to_insert = (0, '1@2000-01-01')
	#cursor.execute(postgres_insert_query, record_to_insert)
	#connection.commit()
	#print(cursor.rowcount, "Record inserted successfully into tbl_tfloatinst table")

	#cursor.execute(postgres_insert_query, rows[3])

	postgres_insert_query = ''' INSERT INTO tbl_tfloatinst_temp (k) VALUES (%s) '''

	# executemany() to insert multiple rows rows
	#result = cursor.executemany(postgres_insert_query, rows)
	#connection.commit()

	######################
	# TFloatI
	######################

	postgreSQL_select_Query = "select * from tbl_tfloati order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tfloati table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tfloati =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	######################
	# TFloatSeq
	######################

	postgreSQL_select_Query = "select * from tbl_tfloatseq order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tfloatseq table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tfloatseq =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	######################
	# TFloatS
	######################

	postgreSQL_select_Query = "select * from tbl_tfloats order by k limit 10"

	cursor.execute(postgreSQL_select_Query)
	print("Selecting rows from tbl_tfloats table using cursor.fetchall")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tfloats =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

except psycopg2.DatabaseError as e:

	print('Error {e}')

finally:

	if connectionObject:
		connectionObject.close()
