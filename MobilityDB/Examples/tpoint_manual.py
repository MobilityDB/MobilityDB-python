from MobilityDB import *

print('\n# Create new TGEOMPOINT instances')
var = TGEOMPOINTINST('Point(1 1)@2019-09-08')
print(var)
var = TGEOMPOINTI('{Point(1 1)@2019-09-08, Point(2 2)@2019-09-09, Point(1 1)@2019-09-10}')
print(var)
var = TGEOMPOINTSEQ('[Point(1 1)@2019-09-08, Point(2 2)@2019-09-09, Point(1 1)@2019-09-10]')
print(var)
var = TGEOMPOINTS('{[Point(1 1)@2019-09-08, Point(2 2)@2019-09-09, Point(1 1)@2019-09-10],'
    '[Point(1 1)@2019-09-11, Point(2 2)@2019-09-12]}')
print(var)

print('\n# Create new TGEOGPOINT instances')
var = TGEOMPOINTINST('Point(1 1)@2019-09-08')
print(var)
var = TGEOGPOINTI('{Point(1 1)@2019-09-08, Point(2 2)@2019-09-09, Point(1 1)@2019-09-10}')
print(var)
var = TGEOGPOINTSEQ('[Point(1 1)@2019-09-08, Point(2 2)@2019-09-09, Point(1 1)@2019-09-10]')
print(var)
var = TGEOGPOINTS('{[Point(1 1)@2019-09-08, Point(2 2)@2019-09-09, Point(1 1)@2019-09-10],'
    '[Point(1 1)@2019-09-11, Point(2 2)@2019-09-12]}')
print(var)


