import asyncio
from mobilitydb.asyncpg import register
from mobilitydb.examples.db_connect import asyncpg_connect

async def run():

    # Set the connection parameters to PostgreSQL
    connection = await asyncpg_connect()

    try:
        # Register MobilityDB data types
        await register(connection)

        ######################
        # TBox
        ######################

        select_query = "SELECT * FROM tbl_tbox ORDER BY k LIMIT 10"

        print("\n****************************************************************")
        print("Selecting rows from tbl_tbox table\n")
        rows = await connection.fetch(select_query)

        for row in rows:
            print("key =", row[0])
            print("tbox =", row[1])
            if not row[1]:
                print("")
            else:
                print("tmin =", row[1].tmin, "\n")

        drop_table_query = "DROP TABLE IF EXISTS tbl_tbox_temp;"
        await connection.execute(drop_table_query)
        print("Table deleted successfully in PostgreSQL ")

        create_table_query = '''CREATE TABLE tbl_tbox_temp
            (
              k integer PRIMARY KEY,
              box tbox
            ); '''

        await connection.execute(create_table_query)
        print("Table created successfully in PostgreSQL ")

        postgres_insert_query = "INSERT INTO tbl_tbox_temp (k, box) VALUES ($1, $2)"
        await connection.executemany(postgres_insert_query, rows)
        # count = cursor.rowcount
        print(len(rows), "record(s) inserted successfully into tbl_tbox_temp table")

        ######################
        # STBox
        ######################

        select_query = "SELECT * FROM tbl_stbox ORDER BY k LIMIT 10"

        print("\n****************************************************************")
        print("Selecting rows from tbl_stbox table\n")
        rows = await connection.fetch(select_query)

        for row in rows:
            print("key =", row[0])
            print("stbox =", row[1])
            if not row[1]:
                print("")
            else:
                print("tmin =", row[1].tmin, "\n")

        drop_table_query = "DROP TABLE IF EXISTS tbl_stbox_temp;"
        await connection.execute(drop_table_query)
        print("Table deleted successfully in PostgreSQL ")

        create_table_query = '''CREATE TABLE tbl_stbox_temp
            (
              k integer PRIMARY KEY,
              box stbox
            ); '''

        await connection.execute(create_table_query)
        print("Table created successfully in PostgreSQL ")

        postgres_insert_query = "INSERT INTO tbl_stbox_temp (k, box) VALUES ($1, $2)"
        await connection.executemany(postgres_insert_query, rows)
        # count = cursor.rowcount
        print(len(rows), "record(s) inserted successfully into tbl_stbox_temp table")

        print("\n****************************************************************")

    finally:
        await connection.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())


