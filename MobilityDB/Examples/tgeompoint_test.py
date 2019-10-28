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
    print(colVal.getValues())
    print("Start Instant:", colVal.startInstant(), "End Instant: ", colVal.endInstant())

    # You can insert
    cursor.execute('create table if not exists tpoint_test(tpoint tgeompoint)')
    cursor.execute('insert into tpoint_test(tpoint) values(%s)' % colVal)
    # Retrieve the results will be the same as above

    # Test the constructor of tgeompointinst. Now I am reading a string (Point can be text or wkb).
    # I can also define the structure as TGEOMPOINT[Point(1,2)@time] without the need for defining this inside a string
    t1 = TGEOMPOINT('point(1 1)@2019-09-09')
    print(t1.startInstant())
    print(t1.getTimestamp())

except psycopg2.DatabaseError as e:

    print('Error {e}')

finally:

    if connectionObject:
        connectionObject.close()
