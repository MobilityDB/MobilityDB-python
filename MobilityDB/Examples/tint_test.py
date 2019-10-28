from MobilityDB import *

connectionObject = None

try:
    # Set the connection parameters to PostgreSQL
    connectionObject = psycopg2.connect(host='127.0.0.1', database='sf0_005', user='postgres', password='ulb')
    connectionObject.autocommit = True

    # Register MobilityDB data types
    MobilityDBRegister(connectionObject)

    cursor = connectionObject.cursor()
    """
    var1 = TINT('{10@2019-09-08, 20@2019-09-09, 20@2019-09-10}')
    print(var1.getValues())
    print(var1.timespan())
    print(var1.getType())
    print(var1.startValue())
    print(var1.instantN(1))
    """

    var1 = TINTS('{[10@2019-09-08, 20@2019-09-09], [20@2019-09-10]}')
    print(var1.sequenceN(0))

except psycopg2.DatabaseError as e:

    print('Error {e}')

finally:

    if connectionObject:
        connectionObject.close()
