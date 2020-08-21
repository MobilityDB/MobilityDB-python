# MobilityDB-python
MobilityDB-python is a database adapter to access [MobilityDB](https://github.com/MobilityDB/MobilityDB) from Python. It supports both the [psycopg2](https://github.com/psycopg/psycopg2) and the [asyncpg](https://github.com/MagicStack/asyncpg) adapters for PostgreSQL and uses the [postgis](https://github.com/tilery/python-postgis) adapter for PostGIS.


Install
------------
```sh
pip install python-mobilitydb
```

Requirements
------------
 - Python >= 3.0
 - MobilityDB

Basic Usage
------------

Using the psycopg2 adapter for PostgreSQL

```python
import psycopg2
from mobilitydb.psycopg import register

connection = None

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
    if connection:
        connection.close()
```

Using the asyncg adapter for PostgreSQL

```python
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
```

Manual
------

HTML: https://docs.mobilitydb.com/MobilityDB-python/master/

PDF: https://docs.mobilitydb.com/MobilityDB-python/master/python-mobilitydb.pdf

EPUB: https://docs.mobilitydb.com/MobilityDB-python/master/python-mobilitydb.epub

Contributing
------------

[Issues](https://github.com/MobilityDB/MobilityDB-python/issues) and [Pull Requests](https://github.com/MobilityDB/MobilityDB-python/pulls) are welcome.

Related Project
---------------

[MobilityDB SQLAlchemy](https://github.com/adonmo/mobilitydb-sqlalchemy) is another package that provides extensions to [SQLAlchemy](https://www.sqlalchemy.org/) for interacting with [MobilityDB](https://github.com/MobilityDB/MobilityDB). 
