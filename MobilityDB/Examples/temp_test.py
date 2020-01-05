
import re
#from parsec import *
from MobilityDB.TemporalTypes.temporal_parser import *
from datetime import datetime, timedelta
from bdateutil.parser import parse
from spans.types import floatrange
from postgis import Geometry, Point, MultiPoint, LineString, GeometryCollection, MultiLineString
from MobilityDB.TimeTypes import TimestampSet, Period, PeriodSet
from MobilityDB.MainTypes import *
from MobilityDB.BoxTypes import *


"""
value = 'srid = 4326 ; {Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01}'
print(value)
srid = re.search(r'(\d+)', value).group()
print("$$$ srid =", srid)
value1 = re.sub(r'^(SRID|srid)\s*=\s*\d+\s*(;|,)\s*', '', value)
print(value1)

print("\n*****TGeomPointInst*****")

inst = TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01')
print(inst)
print(inst.srid())

inst = TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01', srid=4326)
print(inst)
print(inst.srid())

inst = TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01', srid=4326)
print(inst)
print(inst.srid())

# inst = TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01', srid=1234)
# print(inst)
# print(inst.srid())

print("\n*****TGeomPointI*****")

ti = TGeomPointI('{Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01,'
		'Point(10.0 10.0)@2019-09-03 00:00:00+01}')
print(ti)
print(ti.srid())

ti = TGeomPointI('{Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01,'
		'Point(10.0 10.0)@2019-09-03 00:00:00+01}', srid=4326)
print(ti)
print(ti.srid())
print(inst.srid().__class__)

ti = TGeomPointI('SRID=4326;{Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01,'
				 'Point(10.0 10.0)@2019-09-03 00:00:00+01}')
print(ti)
print(ti.srid())
print(inst.srid().__class__)

#ti = TGeomPointI('SRID=4326;{Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01,'
#				 'Point(10.0 10.0)@2019-09-03 00:00:00+01}', srid=1234)
#print(ti)
#print(ti.srid())

print("\n*****TGeomPointSeq*****")

seq = TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01,'
	'Point(10.0 10.0)@2019-09-03 00:00:00+01]')
print(seq)
print(seq.srid())

seq = TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01,'
	'Point(10.0 10.0)@2019-09-03 00:00:00+01]', srid=4326)
print(seq)
print(seq.srid())

seq = TGeomPointSeq('SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01,'
	'Point(10.0 10.0)@2019-09-03 00:00:00+01]', srid=4326)
print(seq)
print(seq.srid())

#seq = TGeomPointSeq('SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01,'
#	'Point(10.0 10.0)@2019-09-03 00:00:00+01]', srid=1234)
#print(seq)
#print(seq.srid())

print("\n*****TGeomPointS*****")

ts = TGeomPointS('{[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01,'
	'Point(10.0 10.0)@2019-09-03 00:00:00+01]}')
print(ts)
print(ts.srid())

ts = TGeomPointS('{[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01,'
	'Point(10.0 10.0)@2019-09-03 00:00:00+01]}', srid=4326)
print(ts)
print(ts.srid())

seq = TGeomPointS('SRID=4326;{[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01,'
	'Point(10.0 10.0)@2019-09-03 00:00:00+01]}', srid=4326)
print(ts)
print(ts.srid())

#ts = TGeomPointS('SRID=4326;{[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01,'
#	'Point(10.0 10.0)@2019-09-03 00:00:00+01]}', srid=1234)
#print(ts)
#print(ts.srid())

"""

box = TBox('TBOX ((1.0, 2000-01-01), (1.0, 2000-01-01)')
print(repr(box))


box = STBox('STBOX ((1.0, 2.0), (1.0, 2.0))')
print(repr(box))


"""

ti = TBoolI('{True@2019-09-01 00:00:00+01, False@2019-09-02 00:00:00+01, True@2019-09-03 00:00:00+01}')
print(ti)

inst = TBoolInst('True', parse('2000-01-01'))
print(inst)
print(inst.BaseClass)
"""




