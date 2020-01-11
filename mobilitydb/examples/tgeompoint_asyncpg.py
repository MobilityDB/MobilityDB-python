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
        # TGeomPointInst
        ######################

        select_query = "select * from tbl_tgeompointinst order by k limit 10"

        print("\n****************************************************************")
        print("Selecting rows from tbl_tgeompointinst table\n")
        rows = await connection.fetch(select_query)

        for row in rows:
            print("key =", row[0])
            print("tgeompointinst =", row[1])
            if not row[1]:
                print("")
            else:
                print("startTimestamp =", row[1].startTimestamp, "\n")

        drop_table_query = '''DROP TABLE IF EXISTS tbl_tgeompointinst_temp;'''
        await connection.execute(drop_table_query)
        print("Table deleted successfully in PostgreSQL ")
    
        create_table_query = '''CREATE TABLE tbl_tgeompointinst_temp
            (
              k integer PRIMARY KEY,
              temp tgeompoint
            ); '''
    
        await connection.execute(create_table_query)
        print("Table created successfully in PostgreSQL ")
    
        postgres_insert_query = ''' INSERT INTO tbl_tgeompointinst_temp (k, temp) VALUES ($1, $2) '''
        await connection.executemany(postgres_insert_query, rows)
        # count = cursor.rowcount
        print(len(rows), "record(s) inserted successfully into tbl_tgeompointinst table")

        ######################
        # TGeomPointI
        ######################

        select_query = "select * from tbl_tgeompointi order by k limit 10"

        print("\n****************************************************************")
        print("Selecting rows from tbl_tgeompointi table\n")
        rows = await connection.fetch(select_query)

        for row in rows:
            print("key =", row[0])
            print("tgeompointi =", row[1])
            if not row[1]:
                print("")
            else:
                print("startTimestamp =", row[1].startTimestamp, "\n")

        drop_table_query = '''DROP TABLE IF EXISTS tbl_tgeompointi_temp;'''
        await connection.execute(drop_table_query)
        print("Table deleted successfully in PostgreSQL ")
    
        create_table_query = '''CREATE TABLE tbl_tgeompointi_temp
            (
              k integer PRIMARY KEY,
              temp tgeompoint
            ); '''
    
        await connection.execute(create_table_query)
        print("Table created successfully in PostgreSQL ")
    
        postgres_insert_query = ''' INSERT INTO tbl_tgeompointi_temp (k, temp) VALUES ($1, $2) '''
        await connection.executemany(postgres_insert_query, rows)
        #count = cursor.rowcount
        print(len(rows), "record(s) inserted successfully into tbl_tgeompointi_temp table")

        ######################
        # TGeomPointSeq
        ######################
    
        select_query = "select * from tbl_tgeompointseq order by k limit 10"
    
        print("\n****************************************************************")
        print("Selecting rows from tbl_tgeompointseq table\n")
        rows = await connection.fetch(select_query)
    
        for row in rows:
            print("key =", row[0])
            print("tgeompointseq =", row[1])
            if not row[1]:
                print("")
            else:
                print("startTimestamp =", row[1].startTimestamp, "\n")
    
        drop_table_query = '''DROP TABLE IF EXISTS tbl_tgeompointseq_temp;'''
        await connection.execute(drop_table_query)
        print("Table deleted successfully in PostgreSQL ")
    
        create_table_query = '''CREATE TABLE tbl_tgeompointseq_temp
            (
              k integer PRIMARY KEY,
              temp tgeompoint
            ); '''
    
        await connection.execute(create_table_query)
        print("Table created successfully in PostgreSQL ")
    
        postgres_insert_query = ''' INSERT INTO tbl_tgeompointseq_temp (k, temp) VALUES ($1, $2) '''
        await connection.executemany(postgres_insert_query, rows)
        #count = cursor.rowcount
        print(len(rows), "record(s) inserted successfully into tbl_tgeompointseq_temp table")

        ######################
        # TGeomPointS
        ######################
    
        select_query = "select * from tbl_tgeompoints order by k limit 10"
    
        print("\n****************************************************************")
        print("Selecting rows from tbl_tgeompoints table\n")
        rows = await connection.fetch(select_query)
    
        for row in rows:
            print("key =", row[0])
            print("tgeompoints =", row[1])
            if not row[1]:
                print("")
            else:
                print("startTimestamp =", row[1].startTimestamp, "\n")
    
        drop_table_query = '''DROP TABLE IF EXISTS tbl_tgeompoints_temp;'''
        await connection.execute(drop_table_query)
        print("Table deleted successfully in PostgreSQL ")
    
        create_table_query = '''CREATE TABLE tbl_tgeompoints_temp
            (
              k integer PRIMARY KEY,
              temp tgeompoint
            ); '''
    
        await connection.execute(create_table_query)
        print("Table created successfully in PostgreSQL ")
    
        postgres_insert_query = ''' INSERT INTO tbl_tgeompoints_temp (k, temp) VALUES ($1, $2) '''
        await connection.executemany(postgres_insert_query, rows)
        # count = cursor.rowcount
        print(len(rows), "record(s) inserted successfully into tbl_tgeompoints_temp table")
    
        print("\n****************************************************************")

    finally:
        await connection.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())


