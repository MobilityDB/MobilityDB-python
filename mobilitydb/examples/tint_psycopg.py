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
    # TIntInst
    ######################

    select_query = "select * from tbl_tintinst order by k limit 10"

    cursor.execute(select_query)
    print("\n****************************************************************")
    print("Selecting rows from tbl_tintinst table\n")
    rows = cursor.fetchall()

    for row in rows:
        print("key =", row[0])
        print("tintinst =", row[1])
        if not row[1]:
            print("")
        else:
            print("startTimestamp =", row[1].startTimestamp, "\n")

        drop_table_query = '''DROP TABLE IF EXISTS tbl_tintinst_temp;'''
        cursor.execute(drop_table_query)
        connection.commit()
        print("Table deleted successfully in PostgreSQL ")

        create_table_query = '''CREATE TABLE tbl_tintinst_temp
            (
              k integer PRIMARY KEY,
              temp tint
            ); '''

        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully in PostgreSQL ")

        postgres_insert_query = ''' INSERT INTO tbl_tintinst_temp (k, temp) VALUES (%s, %s) '''
        result = cursor.executemany(postgres_insert_query, rows)
        connection.commit()
        count = cursor.rowcount
        print(count, "record(s) inserted successfully into tbl_tintinst_temp table")

    ######################
    # TIntI
    ######################

    select_query = "select * from tbl_tinti order by k limit 10"

    cursor.execute(select_query)
    print("\n****************************************************************")
    print("Selecting rows from tbl_tinti table\n")
    rows = cursor.fetchall()

    for row in rows:
        print("key =", row[0])
        print("tinti =", row[1])
        if not row[1]:
            print("")
        else:
            print("startTimestamp =", row[1].startTimestamp, "\n")

        drop_table_query = '''DROP TABLE IF EXISTS tbl_tinti_temp;'''
        cursor.execute(drop_table_query)
        connection.commit()
        print("Table deleted successfully in PostgreSQL ")

        create_table_query = '''CREATE TABLE tbl_tinti_temp
            (
              k integer PRIMARY KEY,
              temp tint
            ); '''

        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully in PostgreSQL ")

        postgres_insert_query = ''' INSERT INTO tbl_tinti_temp (k, temp) VALUES (%s, %s) '''
        result = cursor.executemany(postgres_insert_query, rows)
        connection.commit()
        count = cursor.rowcount
        print(count, "record(s) inserted successfully into tbl_tinti_temp table")

    ######################
    # TIntSeq
    ######################

    select_query = "select * from tbl_tintseq order by k limit 10"

    cursor.execute(select_query)
    print("\n****************************************************************")
    print("Selecting rows from tbl_tintseq table\n")
    rows = cursor.fetchall()

    for row in rows:
        print("key =", row[0])
        print("tintseq =", row[1])
        if not row[1]:
            print("")
        else:
            print("startTimestamp =", row[1].startTimestamp, "\n")

        drop_table_query = '''DROP TABLE IF EXISTS tbl_tintseq_temp;'''
        cursor.execute(drop_table_query)
        connection.commit()
        print("Table deleted successfully in PostgreSQL ")

        create_table_query = '''CREATE TABLE tbl_tintseq_temp
            (
              k integer PRIMARY KEY,
              temp tint
            ); '''

        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully in PostgreSQL ")

        postgres_insert_query = ''' INSERT INTO tbl_tintseq_temp (k, temp) VALUES (%s, %s) '''
        result = cursor.executemany(postgres_insert_query, rows)
        connection.commit()
        count = cursor.rowcount
        print(count, "record(s) inserted successfully into tbl_tintseq_temp table")

    ######################
    # TIntS
    ######################

    select_query = "select * from tbl_tints order by k limit 10"

    cursor.execute(select_query)
    print("\n****************************************************************")
    print("Selecting rows from tbl_tints table\n")
    rows = cursor.fetchall()

    for row in rows:
        print("key =", row[0])
        print("tints =", row[1])
        if not row[1]:
            print("")
        else:
            print("startTimestamp =", row[1].startTimestamp, "\n")

    drop_table_query = '''DROP TABLE IF EXISTS tbl_tints_temp;'''
    cursor.execute(drop_table_query)
    connection.commit()
    print("Table deleted successfully in PostgreSQL ")

    create_table_query = '''CREATE TABLE tbl_tints_temp
        (
          k integer PRIMARY KEY,
          temp tint
        ); '''

    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

    postgres_insert_query = ''' INSERT INTO tbl_tints_temp (k, temp) VALUES (%s, %s) '''
    result = cursor.executemany(postgres_insert_query, rows)
    connection.commit()
    count = cursor.rowcount
    print(count, "record(s) inserted successfully into tbl_tints_temp table")

    print("\n****************************************************************")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:

    if connection:
        connection.close()
