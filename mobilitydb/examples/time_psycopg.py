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
    # TimestampSet
    ######################

    select_query = "SELECT * FROM tbl_timestampset ORDER BY k LIMIT 10"

    cursor.execute(select_query)
    print("\n****************************************************************")
    print("Selecting rows from tbl_timestampset table\n")
    rows = cursor.fetchall()

    for row in rows:
        print("key =", row[0])
        print("timestampset =", row[1])
        if not row[1]:
            print("")
        else:
            print("timespan =", row[1].timespan, "\n")

    drop_table_query = "DROP TABLE IF EXISTS tbl_timestampset_temp;"
    cursor.execute(drop_table_query)
    connection.commit()
    print("Table deleted successfully in PostgreSQL")

    create_table_query = '''CREATE TABLE tbl_timestampset_temp
    (
      k integer PRIMARY KEY,
      ts timestampset
    ); '''
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL")

    insert_query = "INSERT INTO tbl_timestampset_temp (k, ts) VALUES (%s, %s)"
    result = cursor.executemany(insert_query, rows)
    connection.commit()
    count = cursor.rowcount
    print(count, "record(s) inserted successfully into tbl_timestampset_temp table")

    ######################
    # Period
    ######################

    select_query = "SELECT * FROM tbl_period ORDER BY k LIMIT 10"

    cursor.execute(select_query)
    print("\n****************************************************************")
    print("Selecting rows from tbl_period table\n")
    rows = cursor.fetchall()

    for row in rows:
        print("key =", row[0])
        print("period =", row[1])
        if not row[1]:
            print("")
        else:
            print("timespan =", row[1].timespan, "\n")

    drop_table_query = "DROP TABLE IF EXISTS tbl_period_temp;"
    cursor.execute(drop_table_query)
    connection.commit()
    print("Table deleted successfully in PostgreSQL")

    create_table_query = '''CREATE TABLE tbl_period_temp
    (
      k integer PRIMARY KEY,
      p period
    ); '''
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL")

    insert_query = "INSERT INTO tbl_period_temp (k, p) VALUES (%s, %s)"
    result = cursor.executemany(insert_query, rows)
    connection.commit()
    count = cursor.rowcount
    print(count, "record(s) inserted successfully into tbl_period_temp table")

    ######################
    # PeriodSet
    ######################

    select_query = "SELECT * FROM tbl_periodset ORDER BY k LIMIT 10"

    cursor.execute(select_query)
    print("\n****************************************************************")
    print("Selecting rows from tbl_periodset table\n")
    rows = cursor.fetchall()

    for row in rows:
        print("key =", row[0])
        print("periodset =", row[1])
        if not row[1]:
            print("")
        else:
            print("timespan =", row[1].timespan, "\n")


    drop_table_query = "DROP TABLE IF EXISTS tbl_periodset_temp;"
    cursor.execute(drop_table_query)
    connection.commit()
    print("Table deleted successfully in PostgreSQL")

    create_table_query = '''CREATE TABLE tbl_periodset_temp
    (
      k integer PRIMARY KEY,
      ps periodset
    ); '''
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL")

    insert_query = "INSERT INTO tbl_periodset_temp (k, ps) VALUES (%s, %s)"
    result = cursor.executemany(insert_query, rows)
    connection.commit()
    count = cursor.rowcount
    print(count, "record(s) inserted successfully into tbl_periodset_temp table")

    print("\n****************************************************************")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:

    if connection:
        connection.close()
