import psycopg2
from MobilityDB import *

connectionObject = None

try:
    # Set the connection parameters to PostgreSQL
    connectionObject = psycopg2.connect(host='127.0.0.1', database='sf0_005', user='postgres', password='')
    connectionObject.autocommit = True

    # Register MobilityDB data types
    MobilityDBRegister(connectionObject)

    cursor = connectionObject.cursor()

    # TGEOMPOINT(Sequence)
    cursor.execute('SELECT trip from trips;')
    colVal = cursor.fetchone()[0]
    print(colVal)
    print(colVal.getValue())
    print("Start Instant:", colVal.startInstant(), "End Instant: ", colVal.endInstant())

    # Test the constructor of tgeompointinst. Now I am reading a string (Point can be text or wkb).
    # I can also define the structure as TGEOMPOINT[Point(1,2)@time] without the need for defining this inside a string
    t1 = TGEOMPOINTINST('point(1 1)@2019-09-09')
    print(t1.getValue())
    print(t1.getTimestamp())

except psycopg2.DatabaseError as e:

    print('Error {e}')

finally:

    if connectionObject:
        connectionObject.close()
