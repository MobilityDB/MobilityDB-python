import asyncio
import asyncpg
from mobilitydb.asyncpg import register
from mobilitydb.examples.db_connect import asyncpg_connect


async def run():

	# Set the connection parameters to PostgreSQL
	connection = await asyncpg_connect()

	try:
		# Register MobilityDB data types
		await register(connection)

		######################
		# TIntInst
		######################

		select_query = "select * from tbl_tintinst order by k limit 10"

		print("\n****************************************************************")
		print("Selecting rows from tbl_tintinst table\n")
		rows = await connection.fetch(select_query)

		for row in rows:
			print("key =", row[0])
			print("tintinst =", row[1])
			if not row[1]:
				print("")
			else:
				print("startTimestamp =", row[1].startTimestamp(), "\n")

		drop_table_query = '''DROP TABLE IF EXISTS tbl_tintinst_temp;'''
		await connection.execute(drop_table_query)
		print("Table deleted successfully in PostgreSQL ")
	
		create_table_query = '''CREATE TABLE tbl_tintinst_temp
			(
			  k integer PRIMARY KEY,
			  temp tint
			); '''
	
		await connection.execute(create_table_query)
		print("Table created successfully in PostgreSQL ")
	
		postgres_insert_query = ''' INSERT INTO tbl_tintinst_temp (k, temp) VALUES ($1, $2) '''
		await connection.executemany(postgres_insert_query, rows)
		# count = cursor.rowcount
		print(len(rows), "record(s) inserted successfully into tbl_tintinst table")

		######################
		# TIntI
		######################

		select_query = "select * from tbl_tinti order by k limit 10"

		print("\n****************************************************************")
		print("Selecting rows from tbl_tinti table\n")
		rows = await connection.fetch(select_query)

		for row in rows:
			print("key =", row[0])
			print("tinti =", row[1])
			if not row[1]:
				print("")
			else:
				print("startTimestamp =", row[1].startTimestamp(), "\n")

		drop_table_query = '''DROP TABLE IF EXISTS tbl_tinti_temp;'''
		await connection.execute(drop_table_query)
		print("Table deleted successfully in PostgreSQL ")
	
		create_table_query = '''CREATE TABLE tbl_tinti_temp
			(
			  k integer PRIMARY KEY,
			  temp tint
			); '''
	
		await connection.execute(create_table_query)
		print("Table created successfully in PostgreSQL ")
	
		postgres_insert_query = ''' INSERT INTO tbl_tinti_temp (k, temp) VALUES ($1, $2) '''
		await connection.executemany(postgres_insert_query, rows)
		#count = cursor.rowcount
		print(len(rows), "record(s) inserted successfully into tbl_tinti_temp table")

		######################
		# TIntSeq
		######################
	
		select_query = "select * from tbl_tintseq order by k limit 10"
	
		print("\n****************************************************************")
		print("Selecting rows from tbl_tintseq table\n")
		rows = await connection.fetch(select_query)
	
		for row in rows:
			print("key =", row[0])
			print("tintseq =", row[1])
			if not row[1]:
				print("")
			else:
				print("startTimestamp =", row[1].startTimestamp(), "\n")
	
		drop_table_query = '''DROP TABLE IF EXISTS tbl_tintseq_temp;'''
		await connection.execute(drop_table_query)
		print("Table deleted successfully in PostgreSQL ")
	
		create_table_query = '''CREATE TABLE tbl_tintseq_temp
			(
			  k integer PRIMARY KEY,
			  temp tint
			); '''
	
		await connection.execute(create_table_query)
		print("Table created successfully in PostgreSQL ")
	
		postgres_insert_query = ''' INSERT INTO tbl_tintseq_temp (k, temp) VALUES ($1, $2) '''
		await connection.executemany(postgres_insert_query, rows)
		#count = cursor.rowcount
		print(len(rows), "record(s) inserted successfully into tbl_tintseq_temp table")

		######################
		# TIntS
		######################
	
		select_query = "select * from tbl_tints order by k limit 10"
	
		print("\n****************************************************************")
		print("Selecting rows from tbl_tints table\n")
		rows = await connection.fetch(select_query)
	
		for row in rows:
			print("key =", row[0])
			print("tints =", row[1])
			if not row[1]:
				print("")
			else:
				print("startTimestamp =", row[1].startTimestamp(), "\n")
	
		drop_table_query = '''DROP TABLE IF EXISTS tbl_tints_temp;'''
		await connection.execute(drop_table_query)
		print("Table deleted successfully in PostgreSQL ")
	
		create_table_query = '''CREATE TABLE tbl_tints_temp
			(
			  k integer PRIMARY KEY,
			  temp tint
			); '''
	
		await connection.execute(create_table_query)
		print("Table created successfully in PostgreSQL ")
	
		postgres_insert_query = ''' INSERT INTO tbl_tints_temp (k, temp) VALUES ($1, $2) '''
		await connection.executemany(postgres_insert_query, rows)
		# count = cursor.rowcount
		print(len(rows), "record(s) inserted successfully into tbl_tints_temp table")
	
		print("\n****************************************************************")

	finally:
		await connection.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())


