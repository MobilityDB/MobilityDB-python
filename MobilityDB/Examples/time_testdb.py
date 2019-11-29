from MobilityDB import *

connectionObject = None

try:
	# Set the connection parameters to PostgreSQL
	connectionObject = psycopg2.connect(host='127.0.0.1', database='sf0_005', user='postgres', password='ulb')
	connectionObject.autocommit = True

	# Register MobilityDB data types
	MobilityDBRegister(connectionObject)

	cursor = connectionObject.cursor()

	t1 = PERIOD('2019-09-08', '2019-09-10')
	print(t1)

	t2 = TIMESTAMPSET('2019-09-08', '2019-09-10', '2019-09-11')
	print(t2)

	t22 = TIMESTAMPSET('2019-09-08', '2019-09-10', '2019-09-11')
	print(t2 == t22)

	t3 = PERIODSET('{[2019-09-08, 2019-09-10], (2019-09-11, 2019-09-12), [2019-09-13), (2019-09-14, 2019-09-15]}')
	print(t3)

except psycopg2.DatabaseError as e:

	print('Error {e}')

finally:

	if connectionObject:
		connectionObject.close()
