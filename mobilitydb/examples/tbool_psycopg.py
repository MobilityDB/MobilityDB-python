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
    # TBoolInst
    ######################

    select_query = "select * from tbl_tboolinst order by k limit 10"

    cursor.execute(select_query)
    print("\n****************************************************************")
    print("Selecting rows from tbl_tboolinst table\n")
    rows = cursor.fetchall()

    for row in rows:
        print("key =", row[0])
        print("tboolinst =", row[1])
        if not row[1]:
            print("")
        else:
            print("startTimestamp =", row[1].startTimestamp, "\n")

    drop_table_query = '''DROP TABLE IF EXISTS tbl_tboolinst_temp;'''
    cursor.execute(drop_table_query)
    connection.commit()
    print("Table deleted successfully in PostgreSQL ")

    create_table_query = '''CREATE TABLE tbl_tboolinst_temp
        (
          k integer PRIMARY KEY,
          temp tbool
        ); '''

    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

    postgres_insert_query = ''' INSERT INTO tbl_tboolinst_temp (k, temp) VALUES (%s, %s) '''
    result = cursor.executemany(postgres_insert_query, rows)
    connection.commit()
    count = cursor.rowcount
    print(count, "record(s) inserted successfully into tbl_tboolinst_temp table")

    ######################
    # TBoolInstSet
    ######################

    select_query = "select * from tbl_tboolinstset order by k limit 10"

    cursor.execute(select_query)
    print("\n****************************************************************")
    print("Selecting rows from tbl_tbooli table\n")
    rows = cursor.fetchall()

    for row in rows:
        print("key =", row[0])
        print("tboolinstset =", row[1])
        if not row[1]:
            print("")
        else:
            print("startTimestamp =", row[1].startTimestamp, "\n")

    drop_table_query = '''DROP TABLE IF EXISTS tbl_tboolinstset_temp;'''
    cursor.execute(drop_table_query)
    connection.commit()
    print("Table deleted successfully in PostgreSQL ")

    create_table_query = '''CREATE TABLE tbl_tboolinstset_temp
        (
          k integer PRIMARY KEY,
          temp tbool
        ); '''

    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

    postgres_insert_query = ''' INSERT INTO tbl_tboolinstset_temp (k, temp) VALUES (%s, %s) '''
    result = cursor.executemany(postgres_insert_query, rows)
    connection.commit()
    count = cursor.rowcount
    print(count, "record(s) inserted successfully into tbl_tboolinstset_temp table")

    ######################
    # TBoolSeq
    ######################

    select_query = "select * from tbl_tboolseq order by k limit 10"

    cursor.execute(select_query)
    print("\n****************************************************************")
    print("Selecting rows from tbl_tboolseq table\n")
    rows = cursor.fetchall()

    for row in rows:
        print("key =", row[0])
        print("tboolseq =", row[1])
        if not row[1]:
            print("")
        else:
            print("startTimestamp =", row[1].startTimestamp, "\n")

    drop_table_query = '''DROP TABLE IF EXISTS tbl_tboolseq_temp;'''
    cursor.execute(drop_table_query)
    connection.commit()
    print("Table deleted successfully in PostgreSQL ")

    create_table_query = '''CREATE TABLE tbl_tboolseq_temp
        (
          k integer PRIMARY KEY,
          temp tbool
        ); '''

    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

    postgres_insert_query = ''' INSERT INTO tbl_tboolseq_temp (k, temp) VALUES (%s, %s) '''
    result = cursor.executemany(postgres_insert_query, rows)
    connection.commit()
    count = cursor.rowcount
    print(count, "record(s) inserted successfully into tbl_tboolseq_temp table")

    ######################
    # TBoolS
    ######################

    select_query = "select * from tbl_tboolseqset order by k limit 10"

    cursor.execute(select_query)
    print("\n****************************************************************")
    print("Selecting rows from tbl_tbools table\n")
    rows = cursor.fetchall()

    for row in rows:
        print("key =", row[0])
        print("tbools =", row[1])
        if not row[1]:
            print("")
        else:
            print("startTimestamp =", row[1].startTimestamp, "\n")

    drop_table_query = '''DROP TABLE IF EXISTS tbl_tboolseqset_temp;'''
    cursor.execute(drop_table_query)
    connection.commit()
    print("Table deleted successfully in PostgreSQL ")

    create_table_query = '''CREATE TABLE tbl_tboolseqset_temp
        (
          k integer PRIMARY KEY,
          temp tbool
        ); '''

    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

    postgres_insert_query = ''' INSERT INTO tbl_tboolseqset_temp (k, temp) VALUES (%s, %s) '''
    result = cursor.executemany(postgres_insert_query, rows)
    connection.commit()
    count = cursor.rowcount
    print(count, "record(s) inserted successfully into tbl_tboolseqset_temp table")

    print("\n****************************************************************")


except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:

    if connection:
        connection.close()
