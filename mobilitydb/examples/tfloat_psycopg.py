import psycopg2
from mobilitydb.psycopg import register
from mobilitydb.examples.db_connect import psycopg_connect

connectionObject = None

try:
	# Set the connection parameters to PostgreSQL
	connection = psycopg_connect()
	connection.autocommit = True

	# Register MobilityDB data types
	register(connection)

	cursor = connection.cursor()

	######################
	# TFloatInst
	######################

	select_query = "select * from tbl_tfloatinst order by k limit 10"

	cursor.execute(select_query)
	print("\n****************************************************************")
	print("Selecting rows from tbl_tfloatinst table\n")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tfloatinst =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

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

	postgres_insert_query = ''' INSERT INTO tbl_tfloatinst_temp (k, temp) VALUES (%s, %s) '''
	result = cursor.executemany(postgres_insert_query, rows)
	connection.commit()
	count = cursor.rowcount
	print(count, "record(s) inserted successfully into tbl_tfloatinst table")

	######################
	# TFloatI
	######################

	select_query = "select * from tbl_tfloati order by k limit 10"

	cursor.execute(select_query)
	print("\n****************************************************************")
	print("Selecting rows from tbl_tfloati table\n")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tfloati =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	drop_table_query = '''DROP TABLE IF EXISTS tbl_tfloati_temp;'''
	cursor.execute(drop_table_query)
	connection.commit()
	print("Table deleted successfully in PostgreSQL ")

	create_table_query = '''CREATE TABLE tbl_tfloati_temp
		(
		  k integer PRIMARY KEY,
		  temp tfloat
		); '''

	cursor.execute(create_table_query)
	connection.commit()
	print("Table created successfully in PostgreSQL ")

	postgres_insert_query = ''' INSERT INTO tbl_tfloati_temp (k, temp) VALUES (%s, %s) '''
	result = cursor.executemany(postgres_insert_query, rows)
	connection.commit()
	count = cursor.rowcount
	print(count, "record(s) inserted successfully into tbl_tfloati_temp table")

	######################
	# TFloatSeq
	######################

	select_query = "select * from tbl_tfloatseq order by k limit 10"

	cursor.execute(select_query)
	print("\n****************************************************************")
	print("Selecting rows from tbl_tfloatseq table\n")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tfloatseq =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	drop_table_query = '''DROP TABLE IF EXISTS tbl_tfloatseq_temp;'''
	cursor.execute(drop_table_query)
	connection.commit()
	print("Table deleted successfully in PostgreSQL ")

	create_table_query = '''CREATE TABLE tbl_tfloatseq_temp
		(
		  k integer PRIMARY KEY,
		  temp tfloat
		); '''

	cursor.execute(create_table_query)
	connection.commit()
	print("Table created successfully in PostgreSQL ")

	postgres_insert_query = ''' INSERT INTO tbl_tfloatseq_temp (k, temp) VALUES (%s, %s) '''
	result = cursor.executemany(postgres_insert_query, rows)
	connection.commit()
	count = cursor.rowcount
	print(count, "record(s) inserted successfully into tbl_tfloatseq_temp table")

	######################
	# TFloatS
	######################

	select_query = "select * from tbl_tfloats order by k limit 10"

	cursor.execute(select_query)
	print("\n****************************************************************")
	print("Selecting rows from tbl_tfloats table\n")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tfloats =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	drop_table_query = '''DROP TABLE IF EXISTS tbl_tfloats_temp;'''
	cursor.execute(drop_table_query)
	connection.commit()
	print("Table deleted successfully in PostgreSQL ")

	create_table_query = '''CREATE TABLE tbl_tfloats_temp
		(
		  k integer PRIMARY KEY,
		  temp tfloat
		); '''

	cursor.execute(create_table_query)
	connection.commit()
	print("Table created successfully in PostgreSQL ")

	postgres_insert_query = ''' INSERT INTO tbl_tfloats_temp (k, temp) VALUES (%s, %s) '''
	result = cursor.executemany(postgres_insert_query, rows)
	connection.commit()
	count = cursor.rowcount
	print(count, "record(s) inserted successfully into tbl_tfloats_temp table")

	print("\n****************************************************************")

except (Exception, psycopg2.Error) as error:
	print("Error while connecting to PostgreSQL", error)

finally:

	if connectionObject:
		connectionObject.close()
