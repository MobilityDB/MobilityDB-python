from MobilityDB import *

print('\n# Create new TBOX instances')
var = TBOX(10, '2019-09-08 00:00:00+02', 30, '2019-09-10 00:00:00+02')
print(var)
var = TBOX(10, 30)
print(var)
var = TBOX('2019-09-08 00:00:00+02', '2019-09-10 00:00:00+02')
print(var)

print('\n# Create new STBOX instances')
var = STBOX(10, 50, 20, 60)
print(var)
var = STBOX(10, 50, 100, 20, 60, 200)
print(var)
var = STBOX(10, 50, '2019-09-08 00:00:00+02', 20, 60, '2019-09-10 00:00:00+02')
print(var)
var = STBOX(10, 50, 100, '2019-09-08 00:00:00+02', 20, 60, 200, '2019-09-10 00:00:00+02')
print(var)
var = STBOX('2019-09-08 00:00:00+02', '2019-09-10 00:00:00+02')
print(var)

print('\n# Create new GEODSTBOX instances')
var = GEODSTBOX(10, 50, 100, 20, 60, 200)
print(var)
var = GEODSTBOX(10, 50, 100, '2019-09-08 00:00:00+02', 20, 60, 200, '2019-09-10 00:00:00+02')
print(var)
var = GEODSTBOX('2019-09-08 00:00:00+02', '2019-09-10 00:00:00+02')
print(var)

