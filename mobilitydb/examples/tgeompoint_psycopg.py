import psycopg2
from mobilitydb.psycopg import register
from mobilitydb.examples.db_connect import psycopg_connect

connection = None

try:
	# Set the connection parameters to PostgreSQL
	connection = psycopg_connect()
	connection.autocommit = True

	# Register MobilityDB data types
	register(connection)

	cursor = connection.cursor()

	######################
	# TGeomPointInst
	######################

	select_query = "select * from tbl_tgeompointinst order by k limit 10"

	cursor.execute(select_query)
	print("\n****************************************************************")
	print("Selecting rows from tbl_tgeompointinst table\n")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tgeompointinst =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	drop_table_query = '''DROP TABLE IF EXISTS tbl_tgeompointinst_temp;'''
	cursor.execute(drop_table_query)
	connection.commit()
	print("Table deleted successfully in PostgreSQL ")

	create_table_query = '''CREATE TABLE tbl_tgeompointinst_temp
		(
		  k integer PRIMARY KEY,
		  temp tgeompoint
		); '''

	cursor.execute(create_table_query)
	connection.commit()
	print("Table created successfully in PostgreSQL ")

	postgres_insert_query = ''' INSERT INTO tbl_tgeompointinst_temp (k, temp) VALUES (%s, %s) '''
	result = cursor.executemany(postgres_insert_query, rows)
	connection.commit()
	count = cursor.rowcount
	print(count, "record(s) inserted successfully into tbl_tgeompointinst_temp table")

	######################
	# TGeomPointI
	######################

	select_query = "select * from tbl_tgeompointi order by k limit 10"

	cursor.execute(select_query)
	print("\n****************************************************************")
	print("Selecting rows from tbl_tgeompointi table\n")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tgeompointi =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	drop_table_query = '''DROP TABLE IF EXISTS tbl_tgeompointi_temp;'''
	cursor.execute(drop_table_query)
	connection.commit()
	print("Table deleted successfully in PostgreSQL ")

	create_table_query = '''CREATE TABLE tbl_tgeompointi_temp
		(
		  k integer PRIMARY KEY,
		  temp tgeompoint
		); '''

	cursor.execute(create_table_query)
	connection.commit()
	print("Table created successfully in PostgreSQL ")

	postgres_insert_query = ''' INSERT INTO tbl_tgeompointi_temp (k, temp) VALUES (%s, %s) '''
	result = cursor.executemany(postgres_insert_query, rows)
	connection.commit()
	count = cursor.rowcount
	print(count, "record(s) inserted successfully into tbl_tgeompointi_temp table")

	######################
	# TGeomPointSeq
	######################

	select_query = "select * from tbl_tgeompointseq order by k limit 10"

	cursor.execute(select_query)
	print("\n****************************************************************")
	print("Selecting rows from tbl_tgeompointseq table\n")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tgeompointseq =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	drop_table_query = '''DROP TABLE IF EXISTS tbl_tgeompointseq_temp;'''
	cursor.execute(drop_table_query)
	connection.commit()
	print("Table deleted successfully in PostgreSQL ")

	create_table_query = '''CREATE TABLE tbl_tgeompointseq_temp
		(
		  k integer PRIMARY KEY,
		  temp tgeompoint
		); '''

	cursor.execute(create_table_query)
	connection.commit()
	print("Table created successfully in PostgreSQL ")

	postgres_insert_query = ''' INSERT INTO tbl_tgeompointseq_temp (k, temp) VALUES (%s, %s) '''
	result = cursor.executemany(postgres_insert_query, rows)
	connection.commit()
	count = cursor.rowcount
	print(count, "record(s) inserted successfully into tbl_tgeompointseq_temp table")

	######################
	# TGeomPointS
	######################

	select_query = "select * from tbl_tgeompoints order by k limit 10"

	cursor.execute(select_query)
	print("\n****************************************************************")
	print("Selecting rows from tbl_tgeompoints table\n")
	rows = cursor.fetchall()

	for row in rows:
		print("key =", row[0])
		print("tgeompoints =", row[1])
		if not row[1]:
			print("")
		else:
			print("startTimestamp =", row[1].startTimestamp(), "\n")

	drop_table_query = '''DROP TABLE IF EXISTS tbl_tgeompoints_temp;'''
	cursor.execute(drop_table_query)
	connection.commit()
	print("Table deleted successfully in PostgreSQL ")

	create_table_query = '''CREATE TABLE tbl_tgeompoints_temp
		(
		  k integer PRIMARY KEY,
		  temp tgeompoint
		); '''

	cursor.execute(create_table_query)
	connection.commit()
	print("Table created successfully in PostgreSQL ")

	postgres_insert_query = ''' INSERT INTO tbl_tgeompoints_temp (k, temp) VALUES (%s, %s) '''
	result = cursor.executemany(postgres_insert_query, rows)
	connection.commit()
	count = cursor.rowcount
	print(count, "record(s) inserted successfully into tbl_tgeompoints_temp table")

	print("\n****************************************************************")

except (Exception, psycopg2.Error) as error:
	print("Error while connecting to PostgreSQL", error)

finally:

	if connection:
		connection.close()
