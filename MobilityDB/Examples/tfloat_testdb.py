from MobilityDB import *

connectionObject = None

try:
	# Set the connection parameters to PostgreSQL
	connectionObject = psycopg2.connect(host='127.0.0.1', database='sf0_005', user='postgres', password='ulb')
	connectionObject.autocommit = True

	# Register MobilityDB data types
	MobilityDBRegister(connectionObject)

	cursor = connectionObject.cursor()

	# var = TFLOATS('{[10@2019-09-08, 20@2019-09-09, 20@2019-09-10]}')
	# print(var)

	# var1 = TFLOAT('10@2019-09-08')
	# print(var1)
	# var2 = TFLOATINST('20@2019-09-09')
	# print(var2)

	# var3 = TFLOAT([var1, var2])
	# print(var3)

	var1 = TFLOAT('[10@2019-09-08]')
	print(var1)
	var2 = TFLOAT('[20@2019-09-09]')
	print(var2)

	var3 = TFLOAT([var1, var2])
	print(var3)

except psycopg2.DatabaseError as e:

	print('Error {e}')

finally:

	if connectionObject:
		connectionObject.close()
