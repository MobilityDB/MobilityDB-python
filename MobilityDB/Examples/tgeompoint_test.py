from MobilityDB import *

connectionObject = None

try:
    # Set the connection parameters to PostgreSQL
    #connectionObject = psycopg2.connect(host='127.0.0.1', port=5432, database='sf0_005', user='postgres', password='ulb')
    #connectionObject.autocommit = True

    # Register MobilityDB data types
    #MobilityDBRegister(connectionObject)

    #cursor = connectionObject.cursor()

    # TGEOMPOINT(Sequence)
    #cursor.execute('SELECT trip::tgeogpoint from trips;')
    #colVal = cursor.fetchone()
    #print(colVal[0])
    #t = TGEOMPOINTSEQ('[POINT(-50.5168596804142 -28.210467256605625)@2007-05-29 21:17:36.245000+02:00, POINT(-50.5168596804142 -28.210467256605625)@2007-05-29 22:32:07.970000+02:00]')
    #print(t)
    #print("Start Instant:", colVal.startInstant(), "End Instant: ", colVal.endInstant())

    # You can insert
    #cursor.execute('create table if not exists tpoint_test(tpoint tgeompoint)')
    #cursor.execute('insert into tpoint_test(tpoint) values(%s)' % colVal)
    # Retrieve the results will be the same as above

    # Test the constructor of tgeompointinst. Now I am reading a string (Point can be text or wkb).
    # I can also define the structure as TGEOMPOINT[Point(1,2)@time] without the need for defining this inside a string
    t1 = TGEOMPOINT('[point(1 1)@2019-09-09]', srid=4326)
    print(t1)

    t2 = TGEOMPOINT('[point(1 1)@2019-09-09]', srid=4326)
    inst = t2.startInstant()
    val = inst.getValue()
    print(val)
    print(val.x)
    print(val.y)
    print(inst.getTimestamp())

    var3 = TGEOMPOINT([t1, t2])
    print(var3)


    #print(t1.getTimestamp())

    #t2 = TGEOMPOINTS('{[point(1 1)@2019-09-09]}')
    #print(t2)

except psycopg2.DatabaseError as e:

    print('Error {e}')

finally:

    if connectionObject:
        connectionObject.close()
