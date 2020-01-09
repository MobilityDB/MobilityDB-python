# python-mobilitydb
python-mobilitydb is a database adapter to access [MobilityDB](https://github.com/ULB-CoDE-WIT/MobilityDB) from Python. It supports both the [psycopg2](https://github.com/psycopg/psycopg2) and the [asyncpg](https://github.com/MagicStack/asyncpg) adapters for PostgreSQL and uses the [postgis](https://github.com/tilery/python-postgis) adapter for PostGIS.


Install
------------
    pip install python-mobilitydb
    
Requirements
------------
 - Python >= 3.0
 - MobilityDB
 
Basic Usage
------------

Using the psycopg2 adapter for PostgreSQL

    import psycopg2
    from postgis.psycopg import register
    from mobilitydb.psycopg import register

    connectionObject = None

    try:
        # Set the connection parameters to PostgreSQL
        connection = psycopg2.connect(host='localhost', database='test', user='user', password='pw')
        connection.autocommit = True

        # Register MobilityDB data types
        register(connection)

        # Open a cursor to perform database operations
        cursor = connection.cursor()

        # Query the database and obtain data as Python objects
        select_query = "SELECT * FROM tbl_tfloatseq ORDER BY k LIMIT 10"
        cursor.execute(select_query)
        rows = cursor.fetchall()

        # Print the obtained rows and call a method on the instances
        for row in rows:
            print("key =", row[0])
            print("tfloatseq =", row[1])
            if not row[1]:
                print("")
            else:
                print("startTimestamp =", row[1].startTimestamp(), "\n")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        # Close the connection
        if connectionObject:
            connectionObject.close()

Using the asyncg adapter for PostgreSQL

    import asyncio
    import asyncpg
    from mobilitydb.asyncpg import register


    async def run():
        # Connect to an existing database
        connection = await asyncpg.connect(host='localhost', database='test', user='user', password='pw')

        try:
            # Register MobilityDB data types
            await register(connection)

            # Query the database and obtain data as Python objects
            select_query = "SELECT * FROM tbl_tgeompointseq ORDER BY k LIMIT 10"
            rows = await connection.fetch(select_query)

            # Print the obtained rows and call a method on the instances
            for row in rows:
                print("key =", row[0])
                print("tgeompointseq =", row[1])
                if not row[1]:
                    print("")
                else:
                    print("startTimestamp =", row[1].startTimestamp(), "\n")
        finally:
            # Close the connection
            await connection.close()

    # Launch the process
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

Contributing
------------

[Issues](https://github.com/ULB-CoDE-WIT/python-mobilitydb/issues) and [Pull Requests](https://github.com/ULB-CoDE-WIT/python-mobilitydb/pulls) are welcome.

            
            
        
