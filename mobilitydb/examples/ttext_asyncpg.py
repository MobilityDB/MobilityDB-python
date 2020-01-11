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
        # TTextInst
        ######################

        select_query = "select * from tbl_ttextinst order by k limit 10"

        print("\n****************************************************************")
        print("Selecting rows from tbl_ttextinst table\n")
        rows = await connection.fetch(select_query)

        for row in rows:
            print("key =", row[0])
            print("ttextinst =", row[1])
            if not row[1]:
                print("")
            else:
                print("startTimestamp =", row[1].startTimestamp, "\n")

        drop_table_query = '''DROP TABLE IF EXISTS tbl_ttextinst_temp;'''
        await connection.execute(drop_table_query)
        print("Table deleted successfully in PostgreSQL ")
    
        create_table_query = '''CREATE TABLE tbl_ttextinst_temp
            (
              k integer PRIMARY KEY,
              temp ttext
            ); '''
    
        await connection.execute(create_table_query)
        print("Table created successfully in PostgreSQL ")
    
        postgres_insert_query = ''' INSERT INTO tbl_ttextinst_temp (k, temp) VALUES ($1, $2) '''
        await connection.executemany(postgres_insert_query, rows)
        # count = cursor.rowcount
        print(len(rows), "record(s) inserted successfully into tbl_ttextinst table")

        ######################
        # TTextI
        ######################

        select_query = "select * from tbl_ttexti order by k limit 10"

        print("\n****************************************************************")
        print("Selecting rows from tbl_ttexti table\n")
        rows = await connection.fetch(select_query)

        for row in rows:
            print("key =", row[0])
            print("ttexti =", row[1])
            if not row[1]:
                print("")
            else:
                print("startTimestamp =", row[1].startTimestamp, "\n")

        drop_table_query = '''DROP TABLE IF EXISTS tbl_ttexti_temp;'''
        await connection.execute(drop_table_query)
        print("Table deleted successfully in PostgreSQL ")
    
        create_table_query = '''CREATE TABLE tbl_ttexti_temp
            (
              k integer PRIMARY KEY,
              temp ttext
            ); '''
    
        await connection.execute(create_table_query)
        print("Table created successfully in PostgreSQL ")
    
        postgres_insert_query = ''' INSERT INTO tbl_ttexti_temp (k, temp) VALUES ($1, $2) '''
        await connection.executemany(postgres_insert_query, rows)
        #count = cursor.rowcount
        print(len(rows), "record(s) inserted successfully into tbl_ttexti_temp table")

        ######################
        # TTextSeq
        ######################
    
        select_query = "select * from tbl_ttextseq order by k limit 10"
    
        print("\n****************************************************************")
        print("Selecting rows from tbl_ttextseq table\n")
        rows = await connection.fetch(select_query)
    
        for row in rows:
            print("key =", row[0])
            print("ttextseq =", row[1])
            if not row[1]:
                print("")
            else:
                print("startTimestamp =", row[1].startTimestamp, "\n")
    
        drop_table_query = '''DROP TABLE IF EXISTS tbl_ttextseq_temp;'''
        await connection.execute(drop_table_query)
        print("Table deleted successfully in PostgreSQL ")
    
        create_table_query = '''CREATE TABLE tbl_ttextseq_temp
            (
              k integer PRIMARY KEY,
              temp ttext
            ); '''
    
        await connection.execute(create_table_query)
        print("Table created successfully in PostgreSQL ")
    
        postgres_insert_query = ''' INSERT INTO tbl_ttextseq_temp (k, temp) VALUES ($1, $2) '''
        await connection.executemany(postgres_insert_query, rows)
        #count = cursor.rowcount
        print(len(rows), "record(s) inserted successfully into tbl_ttextseq_temp table")

        ######################
        # TTextS
        ######################
    
        select_query = "select * from tbl_ttexts order by k limit 10"
    
        print("\n****************************************************************")
        print("Selecting rows from tbl_ttexts table\n")
        rows = await connection.fetch(select_query)
    
        for row in rows:
            print("key =", row[0])
            print("ttexts =", row[1])
            if not row[1]:
                print("")
            else:
                print("startTimestamp =", row[1].startTimestamp, "\n")
    
        drop_table_query = '''DROP TABLE IF EXISTS tbl_ttexts_temp;'''
        await connection.execute(drop_table_query)
        print("Table deleted successfully in PostgreSQL ")
    
        create_table_query = '''CREATE TABLE tbl_ttexts_temp
            (
              k integer PRIMARY KEY,
              temp ttext
            ); '''
    
        await connection.execute(create_table_query)
        print("Table created successfully in PostgreSQL ")
    
        postgres_insert_query = ''' INSERT INTO tbl_ttexts_temp (k, temp) VALUES ($1, $2) '''
        await connection.executemany(postgres_insert_query, rows)
        # count = cursor.rowcount
        print(len(rows), "record(s) inserted successfully into tbl_ttexts_temp table")
    
        print("\n****************************************************************")

    finally:
        await connection.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())


