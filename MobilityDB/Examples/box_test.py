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
var = STBOX(10, 50, 100, 20, 60, 200, geodetic=True)
print(var)
var = STBOX(10, 50, 100, '2019-09-08 00:00:00+02', 20, 60, 200, '2019-09-10 00:00:00+02', geodetic=True)
print(var)
var = STBOX('2019-09-08 00:00:00+02', '2019-09-10 00:00:00+02', geodetic=True)
print(var)

var2 = TBOX(10, '2019-09-08 00:00:00+02', 30, '2019-09-10 00:00:00+02')
print(var2)

var3 = TBOX(10, '2019-09-08 00:00:00+02', 30, '2019-09-10 00:00:00+02')
print(var3 == var2)

var2 = TBOX('2019-09-08 00:00:00+02', '2019-09-10 00:00:00+02')
print(var2)

var2 = TBOX(10, 30)
print(var2)

var2 = TBOX('TBOX((10, 2019-09-08 00:00:00+02), (30, 2019-09-10 00:00:00+02))')
print(var2)

var2 = TBOX('TBOX((, 2019-09-08 00:00:00+02), (, 2019-09-10 00:00:00+02))')
print(var2)

var2 = TBOX('TBOX((10, ), (30, ))')
print(var2)

var2 = STBOX('STBOX T((10, 50, 2019-09-08 00:00:00+02), (20, 60, 2019-09-10 00:00:00+02))')
print(var2)

var2 = STBOX('STBOX ZT((10, 50, 100,2019-09-08 00:00:00+02), (20, 60, 200, 2019-09-10 00:00:00+02))')
print(var2)

var2 = STBOX('STBOX Z((10, 50, 100), (20, 60, 200))')
print(var2)

var2 = STBOX('GEODSTBOX T((10, 50, 100,2019-09-08 00:00:00+02), (20, 60, 200, 2019-09-10 00:00:00+02))')
print(var2)

var2 = STBOX('GEODSTBOX((10, 50, 100), (20, 60, 200))')
print(var2)

var2 = STBOX('STBOX ((10, 50), (20, 60))')
print(var2)

var2 = STBOX(10, 50, 20, 60)
print(var2)

var2 = STBOX(10, 50, 100, 20, 60, 200)
print(var2)

var2 = STBOX(10, 50, 100, '2019-09-08 00:00:00+02', 20, 60, 200, '2019-09-10 00:00:00+02')
print(var2)

var2 = STBOX(10, 50, 100, 20, 60, 200, geodetic=True)
print(var2)

var2 = STBOX(10, 50, 100, '2019-09-08 00:00:00+02', 20, 60, 200, '2019-09-10 00:00:00+02', geodetic=False)
print(var2)
