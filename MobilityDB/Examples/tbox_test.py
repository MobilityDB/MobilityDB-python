from MobilityDB import *

connectionObject = None

try:
    # Set the connection parameters to PostgreSQL
    connectionObject = psycopg2.connect(host='127.0.0.1', database='sf0_005', user='postgres', password='ulb')
    connectionObject.autocommit = True

    # Register MobilityDB data types
    MobilityDBRegister(connectionObject)

    cursor = connectionObject.cursor()

    #var2 = TBOX('TBOX((10, 2019-09-08 00:00:00+02), (30, 2019-09-10 00:00:00+02))')
    #print(var2)

    var2 = TBOX('TBOX((, 2019-09-08 00:00:00+02), (, 2019-09-10 00:00:00+02))')
    print(var2)

    var2 = TBOX('TBOX((10, ), (30, ))')
    print(var2)

    cursor.execute('SELECT c1::tbox from tintseq;')
    colVal = cursor.fetchone()
    print(colVal[0])

except psycopg2.DatabaseError as e:

    print('Error {e}')

finally:

    if connectionObject:
        connectionObject.close()
